# Python Datetime Module

[Source](https://www.geeksforgeeks.org/python-datetime-module/)

DateTime module มีทั้งหมด 5 class หลัก

1. `date` – มี attributes ได้แก่ year, month, และ day
2. `time` – มี attributes ได้แก่ hour, minute, second, microsecond, และ tzinfo
3. `datetime` – คือการรวม `date` และ `time` และมี attributes ได้แก่ year, month, day, hour, minute, second, microsecond, and tzinfo
4. `timedelta` – เป็นระยะเวลา (microsecond) ซึ่งเป็นส่วนต่างของ 2 date, time หรือ datetime
5. `tzinfo` – เป็น object สำหรับเก็บข้อมูล time zone

## datetime

Argument `year`, `month`, และ `day` จะต้องกำหนด (mandatory) และ `tzinfo` เป็น None ได้

Range ของ attribute แต่ละตัว:

- MINYEAR <= year <= MAXYEAR
- 1 <= month <= 12
- 1 <= day <= number of days in the given month and year
- 0 <= hour < 24
- 0 <= minute < 60
- 0 <= second < 60
- 0 <= microsecond < 1000000

```python
>>> a = datetime(1999, 12, 12, 12, 12, 12, 342380)
>>> print(a)
1999-12-12 12:12:12.342380
```

## timedelta

```python

>>> from datetime import datetime, timedelta
  
# Using current time
>>> ini_time_for_now = datetime.now()
  
# printing initial_date
>>> print("initial_date", str(ini_time_for_now))
initial_date 2024-07-13 23:45:16.572404
  
# Calculating future dates
# for two years
>>> future_date_after_2yrs = ini_time_for_now + timedelta(days=730)
  
>>> future_date_after_2days = ini_time_for_now + timedelta(days=2)
  
# printing calculated future_dates
>>> print('future_date_after_2yrs:', str(future_date_after_2yrs))
future_date_after_2yrs: 2026-07-13 23:45:16.572404
>>> print('future_date_after_2days:', str(future_date_after_2days))
future_date_after_2days: 2024-07-15 23:45:16.572404
```

## Python datetime.tzinfo()

The `datetime.now()` function จะไม่มีการเก็บข้อมูล time zones
การเก็บข้อมูล time zines จะใช้ `tzinfo` ซึ่งเป็น abstract base case ใน Python

เราสามารถส่ง instance ของ class `tzinfo` ใน constructors ของ object datetime and time เพื่อใช้ในการกำหนด time zones

### Naive and Aware datetime objects

- **Naive datetime objects** หมายถึง datetime object ที่ไม่มีการกำหนดข้อมูล time zone (tzinfo เป็น None)
- **Aware datetime objects** คือ datetime object ทีมีข้อมูล time zone

```python
>>> from zoneinfo import ZoneInfo
>>> from datetime import datetime

>>> dt1 = datetime(2015, 5, 21, 12, 0) 
>>> print(dt1)
2015-05-21 12:00:00
>>> dt2 = datetime(2015, 12, 21, 12, 0, tzinfo = ZoneInfo(key='Asia/Bangkok')) 
>>> print(dt2)
2015-12-21 12:00:00+07:00

>>> print("Naive Object :", dt1.tzname())
Naive Object : None
>>> print("Aware Object :", dt2.tzname())
Aware Object : +07

>>> now_aware = dt1.replace(tzinfo=ZoneInfo(key='UTC'))
>>> print(now_aware)
2015-05-21 12:00:00+00:00
```

## Django - Time zones

[Source](https://docs.djangoproject.com/en/4.2/topics/i18n/timezones/)

ถ้ามีการ enable time zone support (USE_TZ=True) โดย default Django จะบันทึก datetime information ในฐานข้อมูลเป็น UTC เมื่อ query ข้อมูลออกมาก็จะได้เป็น object datetime ที่ time-zone-aware

## Naive and aware datetime objects

อย่างที่รู้กันว่า `datetime.datetime` objects ของ Python นั้นมี attribute `tzinfo` ที่ใช้ในการเก็บข้อมูล time zone โดยถ้ามีการ set ค่า `tzinfo` ก็จะส่งผลให้ datetime object นั้นเป็น time-zone-aware และถ้าไม่มีการ set ค่า `tzinfo` ก็จะเป็น time-zone-naive

Django จะมี `is_aware()` และ `is_naive()` ให้ใช้ในการเช็ค

```python
from django.utils import timezone

now = timezone.now()
```

Source code ของ `timezone.now()`:

```python
def now():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if settings.USE_TZ:
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=utc)
    else:
        return datetime.now()
```

เรามาลองดูตัวอย่างการใช้งานกัน

ก่อนอื่นไปแก้ไขไฟล์ `/week3/settings.py` ดังนี้

```python
...
TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_TZ = True
...
```

เปิด shell ขึ้นมาแล้วลองทำตามด้านล่าง

```python
>>> from zoneinfo import ZoneInfo
>>> from datetime import datetime
>>> from django.utils import timezone

>>> dt1 = datetime(2015, 12, 21, 12, 0, tzinfo=ZoneInfo(key='UTC')) 
>>> print(dt1)
2015-12-21 12:00:00+00:00
>>> timezone.is_aware(dt1)
True

>>> dt1_local = timezone.localtime(dt1)
>>> print(dt1_local)
2015-12-21 19:00:00+07:00

>>> dt2 = datetime(2015, 5, 21, 12, 0) 
>>> print(dt2)
2015-12-21 12:00:00
>>> timezone.is_aware(dt2)
False
>>> timezone.is_naive(dt2)
True

>>> dt2_aware = timezone.make_aware(dt2)
>>> print(dt2_aware)
2015-05-21 12:00:00+07:00
>>> timezone.is_aware(dt2_aware)
True
```


### 1. Query ข้อมูลที่สร้างขึ้นในช่วง 24 ชั่วโมงที่ผ่านมา

    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # กำหนดเวลาปัจจุบันตาม timezone ของโปรเจค
    now = timezone.now()
    
    # เวลาที่ผ่านมา 24 ชั่วโมง
    yesterday = now - timedelta(days=1)
    
    # Query ข้อมูลที่สร้างขึ้นในช่วง 24 ชั่วโมงที่ผ่านมา
    recent_entries = MyModel.objects.filter(created_at__gte=yesterday)` 
    
### 2. Query ข้อมูลที่เกิดในช่วง 7 วันข้างหน้า

    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # กำหนดเวลาปัจจุบันตาม timezone ของโปรเจค
    now = timezone.now()
    
    # เวลาที่จะเกิดใน 7 วันข้างหน้า
    seven_days_later = now + timedelta(days=7)
    
    # Query ข้อมูลที่จะเกิดในช่วง 7 วันข้างหน้า
    upcoming_entries = MyModel.objects.filter(event_date__lte=seven_days_later)`
### 3. Query ข้อมูลที่สร้างขึ้นในช่วงสัปดาห์นี้ (เริ่มจากวันจันทร์)

    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # กำหนดเวลาปัจจุบันตาม timezone ของโปรเจค
    now = timezone.now()
    
    # กำหนดวันเริ่มต้นของสัปดาห์ (วันจันทร์)
    start_of_week = now - timedelta(days=now.weekday())
    
    # Query ข้อมูลที่สร้างขึ้นในช่วงสัปดาห์นี้
    this_week_entries = MyModel.objects.filter(created_at__gte=start_of_week)`
### 4. Query ข้อมูลที่ถูกอัพเดทในช่วง 30 นาทีที่ผ่านมา
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # กำหนดเวลาปัจจุบันตาม timezone ของโปรเจค
    now = timezone.now()
    
    # เวลาที่ผ่านมา 30 นาที
    thirty_minutes_ago = now - timedelta(minutes=30)
    
    # Query ข้อมูลที่ถูกอัพเดทในช่วง 30 นาทีที่ผ่านมา
    recently_updated_entries = MyModel.objects.filter(updated_at__gte=thirty_minutes_ago)`
### 5. Query ข้อมูลที่เกิดในช่วงวันเดียวกันของปีที่แล้ว

    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # กำหนดเวลาปัจจุบันตาม timezone ของโปรเจค
    now = timezone.now()
    
    # กำหนดเวลาของปีที่แล้วในวันเดียวกัน
    last_year_today = now - timedelta(days=365)
    
    # Query ข้อมูลที่เกิดในวันเดียวกันของปีที่แล้ว
    last_year_entries = MyModel.objects.filter(event_date__date=last_year_today.date())`
### ใช้ Zoneinfo


    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    
    
    # เวลาปัจจุบันในเขตเวลาที่กำหนด
    now = datetime.now(tzinfo = ZoneInfo('Asia/Bangkok'))
    
    # เวลาที่ผ่านมา 24 ชั่วโมง
    yesterday = now - timedelta(days=1)
    
    # Query ข้อมูลที่สร้างขึ้นในช่วง 24 ชั่วโมงที่ผ่านมา
    recent_entries = MyModel.objects.filter(created_at__gte=yesterday)`

