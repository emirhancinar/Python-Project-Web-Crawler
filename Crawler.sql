use Crawler
create table Urunler(
urunId int identity primary key ,
urunAdi nvarchar(30) not null,
fiyat int 
)

create table UrunUrl(
urlId  int identity primary key,
urunId int ,
url_ nvarchar(250) not null,
)

Insert into Urunler(urunAdi) values ('kulaklýk')
Insert into Urunler(urunAdi) values ('aaa')  

Select * from Urunler