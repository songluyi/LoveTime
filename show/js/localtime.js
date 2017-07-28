/**
 * Created by liuchao on 2017/7/21.
 */

    var pele=document.createElement("localtime");
    document.body.appendChild(pele);
    pele.innerHTML=NowTime();
//    获取当前时间
function NowTime() {
    var time=new Date();
    var year=time.getFullYear();//获取年
    var month=time.getMonth()+1;//或者月
    var day=time.getDate();//或者天
    var hour=time.getHours();//获取小时
    var minu =time.getMinutes();//获取分钟
    var second=time.getSeconds();//或者秒
    var data=year+"-";
    if(month<10){
        data+="0";
    }
    data+=month+"-";
    if(day<10){
        data+="0"
    }
    data+=day+" ";
    if(hour<10){
        data+="0"
    }
    data+=hour+":";
    if(minu<10){
        data+="0"
    }
    data+=minu+":";
    if(second<10){
        data+="0"
    }
    data+=second;
    return data;
}
function time() {
    pele.innerHTML=NowTime();
}
setInterval(time,1000);
