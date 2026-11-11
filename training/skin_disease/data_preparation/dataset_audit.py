"""Per-class split statistics and suggested class weights for final_dataset."""
import os

DATASET = "final_dataset"
splits = ["train","valid","test"]

def count(folder):
    return len([f for f in os.listdir(folder)
                if f.lower().endswith((".jpg",".png",".jpeg"))])

stats = {}

for s in splits:
    for c in os.listdir(os.path.join(DATASET,s)):
        path = os.path.join(DATASET,s,c)
        if not os.path.isdir(path): continue

        stats.setdefault(c,{})
        stats[c][s] = count(path)

print("\n========== PER CLASS SPLIT ==========\n")

total_per_class = {}

for c,v in stats.items():
    tr = v.get("train",0)
    va = v.get("valid",0)
    te = v.get("test",0)
    tot = tr+va+te
    total_per_class[c]=tot

    print(f"{c}")
    print(f" train {tr} ({tr/tot*100:.1f}%)")
    print(f" valid   {va} ({va/tot*100:.1f}%)")
    print(f" test  {te} ({te/tot*100:.1f}%)")
    print(f" TOTAL {tot}")

    if tot<300:
        print(" ⚠ VERY SMALL CLASS")

    if abs(tr/tot-0.78)>0.1:
        print(" ⚠ Train ratio odd")

    if va==0 or te==0:
        print(" ⚠ Missing valid/test")

    print()

print("\n========== INTER CLASS DISTRIBUTION ==========\n")

total_all=sum(total_per_class.values())

for c,t in sorted(total_per_class.items(),key=lambda x:x[1],reverse=True):
    print(f"{c}: {t} ({t/total_all*100:.1f}%)")

mean = total_all/len(total_per_class)

print("\n========== IMBALANCE CHECK ==========\n")

for c,t in total_per_class.items():
    if t < mean*0.5:
        print(f"⚠ {c} severely underrepresented")

print("\nSuggested class weights:\n")

weights={c:round(mean/t,2) for c,t in total_per_class.items()}
print(weights)

print("\n✅ Dataset audit complete\n")
