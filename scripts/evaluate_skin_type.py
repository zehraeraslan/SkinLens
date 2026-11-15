"""Evaluate the skin type hybrid model with the training-time generator (needs training/skin_type on PYTHONPATH).
Edit the paths below (skin_type/{Train,Validation,Test}, best_hybrid_model.h5)."""
import os,sys,numpy as np
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
sys.path.insert(0,"training/skin_type"); sys.path.insert(0,"scripts")
import tensorflow as tf
from lbp_pipeline import HybridSkinGenerator
from split_utils import base_name, md5
from sklearn.metrics import classification_report, confusion_matrix
g=HybridSkinGenerator("skin_type/Test",batch_size=8,shuffle=False)
m=tf.keras.models.load_model("best_hybrid_model.h5",compile=False)
Ps=[]
for i in range(len(g)):
    (im,lb),_=g[i]; Ps.append(m.predict_on_batch([im,lb]))
P=np.concatenate(Ps); y=g.gen.classes; pr=P.argmax(1); cl=list(g.class_indices)
print("ACC",(pr==y).mean().round(4),"n",len(y)); print(classification_report(y,pr,target_names=cl,digits=2)); print(confusion_matrix(y,pr))
c=P.max(1)
for i,k in enumerate(cl): print(k,"mean conf (all of class)",c[y==i].mean().round(3),"| correct only",c[(y==i)&(pr==y)].mean().round(3))
print("below .7:",(c<0.7).sum(),"acc>=.7:",(pr[c>=0.7]==y[c>=0.7]).mean().round(4))
paths=g.gen.filepaths
tr_b=set();tr_h=set()
for sp in ["Train"]:
    for k in cl:
        for f in os.listdir(f"skin_type/{sp}/{k}"): tr_b.add((k,base_name(f))); tr_h.add(md5(f"skin_type/{sp}/{k}/{f}"))
va_h=set(md5(os.path.join(dp,f)) for dp,_,fs in os.walk("skin_type/Validation") for f in fs if f.lower().endswith(("jpg","jpeg","png")))
ident=np.array([md5(p) in tr_h for p in paths]); ident_tv=np.array([(md5(p) in tr_h) or (md5(p) in va_h) for p in paths])
src=np.array([(cl[i],base_name(os.path.basename(p))) in tr_b for p,i in zip(paths,y)])
print("identical to train:",ident.sum(),"| identical to train/valid:",ident_tv.sum(),"| source shared w/ train (name):",src.sum())
cleanA=~(ident_tv); print("hash-clean n",cleanA.sum(),"acc",(pr[cleanA]==y[cleanA]).mean().round(4), "per-class n",np.bincount(y[cleanA],minlength=4))
cleanB=~(ident_tv|src); print("hash+name-clean n",cleanB.sum(),"acc",(pr[cleanB]==y[cleanB]).mean().round(4),"per-class n",np.bincount(y[cleanB],minlength=4))
print("leaked(name or hash) acc",(pr[~cleanB]==y[~cleanB]).mean().round(4),"n",(~cleanB).sum())
