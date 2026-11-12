import pandas as pd
file_path="results/results.csv"; df=pd.read_csv(file_path)
real_success=df[(df["source"]=="real")&(df["scenario"]=="manual")&(df["status"]=="ok")].index.tolist()
grades=[2,2,2,1]
if len(real_success)!=4: raise ValueError(f"Expected 4 successful real requests, found {len(real_success)}")
for index,grade in zip(real_success,grades): df.loc[index,"answer_grade"]=grade
df.to_csv(file_path,index=False)
print("Grades updated successfully."); print(df.loc[real_success,["request_id","status","answer_grade"]])
