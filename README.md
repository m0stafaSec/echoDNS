# EchoDNS

أداة شاملة للاستعلام عن سجلات DNS مع دعم لـ DNS over HTTPS (DoH) و AXFR.

## المتطلبات

لتثبيت المتطلبات، قم بتنفيذ الأمر التالي:
```bash
pip install -r requirements.txt
```

## طريقة الاستخدام

```bash
python echoDNS.py -d example.com             # استعلام عن جميع سجلات DNS
python echoDNS.py -d example.com -t A        # استعلام عن سجلات A فقط
python echoDNS.py -d example.com --doh       # استخدام DNS over HTTPS
python echoDNS.py -d example.com --axfr -s ns1.example.com  # محاولة نقل المنطقة
```

### الخيارات المتاحة:
- `-d`, `--domain`: النطاق المراد الاستعلام عنه (يمكن تحديد أكثر من نطاق)
- `-t`, `--type`: نوع سجل DNS (مثل A, MX, CNAME)
- `--doh`: استخدام DNS over HTTPS
- `-s`, `--server`: تحديد خادم DNS مخصص
- `--axfr`: تنفيذ نقل المنطقة من خادم الأسماء المحدد
- `--baseurl`: عنوان URL الأساسي لخادم DoH