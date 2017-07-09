/**
 * Created by SLY on 2017/7/9.
 */
var myChart = echarts.init(document.getElementById('chat_hour'));
// 显示标题，图例和空的坐标轴
myChart.setOption({
    title: {
        text: '最爱聊天的时段'
    },
    tooltip: {},
    legend: {
        data:['次数']
    },
    xAxis: {
        data:  []
    },
    yAxis: {},
    series: [{
        name: '次数',
        type: 'bar',
        data: []
    }]
});

// 异步加载数据
$.get('./json/hour.json').done(function (data) {
    myChart.hideLoading();
    // 填入数据
    // 这个字段还是要先被初始化 哪怕是空白也行
    myChart.setOption({
        xAxis: {
        data: data.x_data
        },
        series: [{
            // 根据名字对应到相应的系列
            name: '次数',
            data: data.y_data
        }]
    });
});

var myRatio = echarts.init(document.getElementById('reply_ratio'));
// 显示标题，图例和空的坐标轴
myRatio.setOption(
    {
    title : {
        text: '聊天回复比率',
        subtext: '仅供参考',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:[]
        // data: ['回复TA的比率','回复你的比率']
    },
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                // {value:335, name:'回复TA的比率'},
                // {value:1548, name:'回复你的比率'}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
});

// 异步加载数据
$.get('./json/reply_ratio.json').done(function (data) {
    console.log(data.y_data);
    myRatio.hideLoading();
    // 填入数据
    // 这个字段还是要先被初始化 哪怕是空白也行
    myRatio.setOption({
        legend :{
            data:data.x_data
        },
        series: [{
            // 根据名字对应到相应的系列

            data: data.y_data
        }]
    });
});

