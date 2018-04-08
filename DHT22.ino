#include "DHT.h"  // подключаем библиотеку
 
#define DHTPIN 2 // номер пина, к которому подсоединен датчик
 
// Раскомментировать нужную строку
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
 
DHT dht(DHTPIN, DHTTYPE);     // Инициализация сенсора DHT
 
void setup() {
 
Serial.begin(9600);
dht.begin();
 
}
 
void loop() {
 
// задержка 1,5 секунды между измерениями
 
delay(20000);
 
float h = dht.readHumidity();    // cчитывание влажности
float t = dht.readTemperature();     // cчитывание температуры
 
// проверка NaN (вывод цифровых значений) 
if (isnan(h) || isnan(t)) {
Serial.println("Data error!");
}
else
{
Serial.print (h);
Serial.print (t);
 }
}
