توضیحات :




# مراحل اجرا :
دستورات زیر را از ترمینال و دایرکتری اصلی فایل‌ها اجرا کنید :
python3 -m venv venv
source venv/bin/activate

pip install django pymysql

mysql -u root -p < university_association.sql
python cli.py
نکات قابل توجه :
پسورد دیتابیس در داخل کد 12345 ست شده
