/**
 * Created by SLY on 2017/7/9.
 */
var myTime = echarts.init(document.getElementById('reply_time'));
myTime.setOption({
    title: {
        text: '聊天回复速率',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis'
        // formatter: '{a} <br/>{b} : {c}'
    },
    legend: {
        left: 'left',
        data: ['你的速率', 'TA的速率']
    },
    xAxis: {
        type: 'category',
        name: '日期',
        splitLine: {show: false},
        data: reply_fluency.x_data
    },
    grid: {
        left: '3%',
        right: '10%',
        bottom: '3%',
        containLabel: true
    },
    yAxis: {
        type: 'log',
        name: '间隔分钟'
    },
    series: [
        {
            name: '你的速率',
            type: 'line',
            data: reply_fluency.boy
        },
        {
            name: 'TA的速率',
            type: 'line',
            data: reply_fluency.girl
        }
    ]
});
myTime.resize({width:'710px'});
var myChart = echarts.init(document.getElementById('chat_hour'));
// 显示标题，图例和空的坐标轴
myChart.setOption({
    title: {
        text: '最爱聊天的时段',
        left: 'center'
    },
    tooltip: {},
    legend: {
        data:['次数'],
        left: 'left'
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

// 因为浏览器安全问题弃用异步加载数据
// $.get('./json/hour.json').done(function (data) {
myChart.hideLoading();
// 填入数据
// 这个字段还是要先被初始化 哪怕是空白也行

myChart.setOption({
    xAxis: {
    data: hour.x_data
    },
    series: [{
        // 根据名字对应到相应的系列
        name: '次数',
        data: hour.y_data
    }]
});
// });

var myRatio = echarts.init(document.getElementById('reply_ratio'));
// 显示标题，图例和空的坐标轴
myRatio.setOption(
    {
    title : {
        text: '聊天回复频次比',
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
// $.get('./json/reply_ratio.json').done(function (data) {
myRatio.hideLoading();
// 填入数据
// 这个字段还是要先被初始化 哪怕是空白也行
myRatio.setOption({
    legend :{
        data:reply_ratio.x_data
    },
    series: [{
        // 根据名字对应到相应的系列

        data: reply_ratio.y_data
    }]
});
// });

var myContent = echarts.init(document.getElementById('content_ratio'));
// 显示标题，图例和空的坐标轴
myContent.setOption(
    {
    title : {
        text: '聊天内容长度比率',
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
            name: '频次详细',
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
// $.get('./json/content_ratio.json').done(function (data) {
myContent.hideLoading();
// 填入数据
// 这个字段还是要先被初始化 哪怕是空白也行
myContent.setOption({
    legend :{
        data:content_ratio.x_data
    },
    series: [{
        // 根据名字对应到相应的系列

        data: content_ratio.y_data
    }]
});
// });

function getVirtulData(year) {
    year = year || '2017';
    var date = +echarts.number.parseDate(year + '-01-01');
    var end = +echarts.number.parseDate((+year + 1) + '-01-01');
    var dayTime = 3600 * 24 * 1000;
    var data = [];
    for (var time = date; time < end; time += dayTime) {
        data.push([
            echarts.format.formatTime('yyyy-MM-dd', time),
            Math.floor(Math.random() * 10000)
        ]);
    }
    return data;
}

var data = getVirtulData(2014);
var newData = getVirtulData(2015);
var fuckData=getVirtulData(2016);
console.log(newData);
var myLove = echarts.init(document.getElementById('lovetime'));
var container = document.getElementById('lovetime');
// container.style.height = 1800+'px';
// 显示标题，图例和空的坐标轴
// var resizeMyLove = function () {
//     container.style.width = window.innerWidth+'px';
//     container.style.height = window.innerWidth+'px';
// };
// //设置容器高宽
// resizeMyLove();
// 基于准备好的dom，初始化echarts实例
// console.log(data.sort(function (a, b) {
//                 return b[1] - a[1];
//             }).slice(0, 12));
myLove.setOption(
    {
    backgroundColor: '#404a59',
    title: {
        top: 30,
        text: '聊天日历图',
        subtext: '你开心就好',
        left: 'center',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip : {
        trigger: 'item'
    },
    legend: {
        top: '30',
        left: '100',
        data:['频次', 'Top 12'],
        textStyle: {
            color: '#fff'
        }
    },
    calendar: [{
        top: 100,
        left: 'center',
        range: ['2016-01-01', '2016-6-30'],
        splitLine: {
            show: true,
            lineStyle: {
                color: '#000',
                width: 4,
                type: 'solid'
            }
        },
        yearLabel: {
            formatter: '{start}  1st',
            textStyle: {
                color: '#fff'
            }
        },
        itemStyle: {
            normal: {
                color: '#323c48',
                borderWidth: 1,
                borderColor: '#111'
            }
        }
    }, {
        top: 340,
        left: 'center',
        range: ['2016-06-30', '2017-01-01'],
        splitLine: {
            show: true,
            lineStyle: {
                color: '#000',
                width: 4,
                type: 'solid'
            }
        },
        yearLabel: {
            formatter: '{start}  2nd',
            textStyle: {
                color: '#fff'
            }
        },
        itemStyle: {
            normal: {
                color: '#323c48',
                borderWidth: 1,
                borderColor: '#111'
            }
        }
    },
    {
        top: 580,
        left: 'center',
        range: ['2017-01-01', '2017-06-31'],
        splitLine: {
            show: true,
            lineStyle: {
                color: '#000',
                width: 4,
                type: 'solid'
            }
        },
        yearLabel: {
            formatter: '{start}  1nd',
            textStyle: {
                color: '#fff'
            }
        },
        itemStyle: {
            normal: {
                color: '#323c48',
                borderWidth: 1,
                borderColor: '#111'
            }
        }
    }],

    series : [
        {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            data: data,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
        {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            calendarIndex: 1,
            data: data,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
        {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            data: newData,
            calendarIndex: 1,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
         {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            calendarIndex: 2,
            data: newData,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
               {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            data: fuckData,
            calendarIndex: 3,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
         {
            name: '频次',
            type: 'scatter',
            coordinateSystem: 'calendar',
            calendarIndex: 4,
            data: fuckData,
            symbolSize: function (val) {
                return val[1] / 500;
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            calendarIndex: 0,
            data: data.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },

        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            calendarIndex: 2,
            data: newData.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },
        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            calendarIndex: 1,
            data: newData.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },
        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            data: newData.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },
        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            calendarIndex: 3,
            data: fuckData.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },
        {
            name: 'Top 12',
            type: 'effectScatter',
            coordinateSystem: 'calendar',
            calendarIndex: 4,
            data: fuckData.sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 12),
            symbolSize: function (val) {
                return val[1] / 500;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        }
    ]
});
// 这里就是默认的
var pines_size=function (val) {
                return val[1] / 5;
            };
// 异步加载数据
// $.get('./json/little_pinnes.json').done(function (data) {
var your_size=parseInt(little_pinnes.data)/30;
pines_size=function (val) {
        return val[1] / your_size;
    };
// });

// console.log(pines_size);
// $.get('./json/calendar.json').done(function (data) {
myLove.hideLoading();
// 通过如下进行更改原先宽高大小，仅仅通过style.height 是不行的
myHight=(calendar.data.length)*250+'px';
myLove.resize({height:myHight});
console.log(calendar.calendar);

// 填入数据
// 这个字段还是要先被初始化 哪怕是空白
// myLove.height = (data.data.length)*250+'px';
// container.style.width = (data.data.length)*250+'px';
container.style.height = (calendar.data.length)*250+'px';
for (var one=0,len=calendar.calendar.length; one<len; one++)
{
calendar.calendar[one]["symbolSize"]=pines_size;
console.log(calendar.calendar[one])
}
myLove.setOption({
    calendar :calendar.data,
    series:calendar.calendar

});
// });

