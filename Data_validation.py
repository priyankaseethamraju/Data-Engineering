import pandas as pd
import datetime
data1=pd.read_csv('data.csv')


#crash ID is not null(existence assertion)
crashid_notnull = pd.notnull(data1["Crash ID"])
assert crashid_notnull.all()==True

#crash month or day or year is not null (existence assertion)

try:
    crashyear_notnull = pd.notnull(data1["Crash Year"])
    crashmonth_notnull=pd.notnull(data1["Crash Month"])
    crashday_notnull = pd.notnull(data1["Crash Day"])
    assert (crashday_notnull.all() or crashmonth_notnull.all() or crashyear_notnull.all()) == True

except AssertionError:
    print("assertion error")


#crash month is not invalid i.e, it should be in the range of 1-12 (limit assertion)
try:
    assert (data1["Crash Month"].all() in range(1,13)) == True
except AssertionError:
    print("Assertion error")

#crash id should be numeric(limit assertion)
try:

    assert (data1["Crash ID"].astype(str).str.isnumeric().all()) == True
except AssertionError:
    print("Assertion error")

isValidDate=True
try:
    datetime.datetime(int(data1["Crash Year"].all()),int(data1["Crash Month"].all()),int(data1["Crash Day"].all()))
except ValueError:
    isValidDate=False
print(isValidDate)

column_values = data1[["Serial #","Crash Year","County Code"]].values
try:
 assert pd.Series(data1[column_values]).is_unique
except AssertionError:
    print("assertion errors")
except KeyError:
    print("key error")
