# Question
1. ถ้าสร้าง asyncio.create_task(*tasks) ที่ไม่มี await ที่ main() เกิดอะไรบ้าง
   1. ..Task จะเริ่มรันทันที (หลังจาก event loop ได้โอกาสทำงาน) เพราะ create_task() จะ schedule coroutine ให้ทำงานแบบ background โดยไม่รอผล
   2. ..Main อาจจบก่อน task ทำงานเสร็จ → ถ้า main() จบและ event loop ปิดลงก่อน task ทำเสร็จ งานใน task จะถูกยกเลิก (cancel) หรือหยุดทำทันที
   3. ..ไม่เห็น exception จาก task เพราะไม่มีการ await → ถ้า task ข้างในเกิด error จะไม่ถูก raise ที่ main ทำให้ดีบักยาก (จะเห็นแค่ warning จาก asyncio)
2. ความแตกต่างระหว่าง asyncio.gather(*tasks) กับ asyncio.wait(tasks) คืออะไร
   1. ..gather() จะรวมหลาย coroutine/Task ไว้เป็น coroutine เดียว แล้วคืนค่าผลลัพธ์ทั้งหมดเป็นลิสต์ เรียงตามลำดับที่ส่งเข้าไป
ถ้า task ใด error → gather จะ raise error ทันที (default return_exceptions=False)
   2. ..wait() จะคืน (done, pending) เป็นเซ็ตของ tasks ที่เสร็จแล้วและที่ยังรออยู่ → ต้อง loop เช็กเอง และไม่ได้คืนค่าของ task โดยตรง
ใช้ได้กับหลาย mode เช่น FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED
   3. ..พฤติกรรมการหยุดรอ
gather() จะรอให้ทุก task เสร็จ (เว้นแต่ task บางอัน raise error)
wait() สามารถหยุดเมื่อบาง task เสร็จได้ (ตาม mode ที่กำหนด) และให้จัดการต่อเอง
3. สร้าง create_task() และ coroutine ของ http ให้อะไรต่างกัน
   1. ..create_task() แปลง coroutine เป็น Task → coroutine จะถูก schedule ให้รันทันทีใน event loop โดยไม่ต้อง await ตอนสร้าง
   2. ..coroutine HTTP (เช่น session.get(url)) เป็นแค่ awaitable object → จะไม่เริ่มทำงานจนกว่าจะ await หรือถูก wrap เป็น Task
   3. ..การจัดการ concurrent
ถ้าสร้าง coroutine เฉย ๆ แล้ว await ทีละตัว → ทำงานแบบ sequential
ถ้าสร้างด้วย create_task() แล้วรวมหลายตัว → สามารถรัน concurrent ได้จริง
