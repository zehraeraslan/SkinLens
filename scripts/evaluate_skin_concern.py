import os,sys,re,hashlib,numpy as np
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import tensorflow as tf
from split_utils import base_name, md5
from sklearn.metrics import classification_report, confusion_matrix
root="data/skin_concern"; classes=sorted(os.listdir(f"{root}/train"))  # keras alphabetical (uppercase first)
print(classes)
tr_b=set();tr_h=set()
for c in classes:
    for f in os.listdir(f"{root}/train/{c}"):
        if f.lower().endswith(".jpg"): tr_b.add((c,base_name(f))); tr_h.add(md5(f"{root}/train/{c}/{f}"))
files=[];Y=[];clean=[]
for i,c in enumerate(classes):
    for f in sorted(os.listdir(f"{root}/test/{c}")):
        p=f"{root}/test/{c}/{f}"; files.append(p);Y.append(i); clean.append((c,base_name(f)) not in tr_b and md5(p) not in tr_h)
Y=np.array(Y);clean=np.array(clean)
X=np.stack([tf.keras.utils.img_to_array(tf.keras.utils.load_img(p,target_size=(224,224))) for p in files])
print("test",len(Y),"clean",clean.sum())
for m in ["models/skin_concern_final_model.keras"]:
    print("\n=====",m)
    try:
        model=tf.keras.models.load_model(m,compile=False,safe_mode=False)
    except Exception as e:
        print("LOAD FAIL",str(e)[:300]); continue
    print("inputs",[i.shape for i in model.inputs],"out",model.output_shape,"layers",len(model.layers),"names",[l.name for l in model.layers[:4]],"params",model.count_params())
    if len(model.inputs)>1: print("multi-input; skip"); continue
    P=model.predict(X,batch_size=32,verbose=0);pr=P.argmax(1)
    print("acc all",(pr==Y).mean().round(4),"clean",(pr[clean]==Y[clean]).mean().round(4))
    if "skin_concern_final" in m:
        print(classification_report(Y,pr,target_names=classes,digits=2));print(confusion_matrix(Y,pr))
        print("clean report");print(classification_report(Y[clean],pr[clean],target_names=classes,digits=2))
        c=P.max(1);print("conf mean",c.mean().round(3),"<0.7:",(c<0.7).sum())
