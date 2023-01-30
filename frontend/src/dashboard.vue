<template>
  <div>
    <orgprovider v-model="selectedOrg">
    </orgprovider>

    <div style="margin-top:30px;">
      <!-- Container-fluid starts-->
      <div class="container-fluid">
        <div class="row second-chart-list third-news-update">

          <div class="col-xl-12 xl-100 dashboard-sec box-col-12">
            <px-card class="earning-card">
              <div class="row m-0">
                <div class="col-xl-2 earning-content p-0">
                  <div class="row m-0 chart-left">
                    <div class="col-xl-12 p-0">
                      <h5>Dashboard</h5>
                      <p class="font-roboto">Overview of last month across all contracts</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning">
                      <h5>{{ stats.transactions_24h }}</h5>
                      <p class="font-roboto">24h Transactions</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning" style="text-align: initial!important">
                      <h5>{{ stats.transactions_7d }}</h5>
                      <p class="font-roboto">7d Transactions</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning">
                      <h5>{{ stats.transactions_30d }}</h5>
                      <p class="font-roboto">30d Transactions</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning">
                      <h5>{{ stats.users_24h }}</h5>
                      <p class="font-roboto">24h Verified Users</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning">
                      <h5>{{ stats.users_7d }}</h5>
                      <p class="font-roboto">7d Verified Users</p>
                    </div>
                    <div class="col-xl-12 p-0 left_side_earning">
                      <h5>{{ stats.users_30d }}</h5>
                      <p class="font-roboto">30d Verified Users</p>
                    </div>
                  </div>
                </div>
                <div class="col-xl-5 earning-content p-0">
                  <LineChart title="Transactions by Contract (30d)" style="min-width:1000px" :breakdowns="txBreakdowns" />
                </div>
                <div class="col-xl-5 earning-content p-0">
                  <LineChart title="Connected Users by Contract (30d)" style="min-width:1000px" :breakdowns="walletBreakdowns" />
                </div>
              </div>
            </px-card>
          </div>
          <div class="col-xl-9 xl-100 chart_data_left box-col-12">

          </div>
        </div>
      </div>
      <!-- Container-fluid Ends-->
    </div>
  </div>

</template>
<script>

import LineChart from "@/components/linechart.vue";
import Orgprovider from "@/components/orgprovider.vue";

var primary = localStorage.getItem('primary_color') || '#7366ff';
var secondary = localStorage.getItem('secondary_color') || '#f73164';


export default {
  name : 'Dashboard',
  components: {Orgprovider, LineChart},

  data() {
    return {
      selectedOrg: null,
      events: [
        {
          title  : 'event1',
          start  : '2010-01-01',
        },
        {
          title  : 'event2',
          start  : '2010-01-05',
          end    : '2010-01-07',
        },
        {
          title  : 'event3',
          start  : '2010-01-09T12:30:00',
          allDay : false,
        },
      ],
      smallchart1: {
        chartData_1: {
          labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
          series: [
            [400, 900, 800, 1000, 700, 1200, 300],
            [1000, 500, 600, 400, 700, 200, 1100],
          ],
        },
        chartOptions: {
          stackBars: true,
          axisX: {
            showGrid: false,
            showLabel: false,
            offset: 0,
          },
          axisY: {
            low: 0,
            showGrid: false,
            showLabel: false,
            offset: 0,
            labelInterpolationFnc: function (value) {
              return value / 1000 + 'k';
            },
          },
        },
        eventHandlers: [
          {
            event: 'draw',
            fn(data) {
              if (data.type === 'bar') {
                data.element.attr({
                  style: 'stroke-width: 3px',
                });
              }
            },
          },
        ],
      },
      smallchart2: {
        chartData_1: {
          labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
          series: [
            [400, 600, 900, 800, 1000, 1200, 500],
            [1000, 800, 500, 600, 400, 200, 900],
          ],
        },
        chartOptions: {
          stackBars: true,
          axisX: {
            showGrid: false,
            showLabel: false,
            offset: 0,
          },
          axisY: {
            low: 0,
            showGrid: false,
            showLabel: false,
            offset: 0,
            labelInterpolationFnc: function (value) {
              return value / 1000 + 'k';
            },
          },
        },
        eventHandlers: [
          {
            event: 'draw',
            fn(data) {
              if (data.type === 'bar') {
                data.element.attr({
                  style: 'stroke-width: 3px',
                });
              }
            },
          },
        ],
      },
      smallchart3: {
        chartData_1: {
          labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
          series: [
            [1100, 900, 600, 1000, 700, 1200, 300],
            [300, 500, 800, 400, 700, 200, 1100],
          ],
        },
        chartOptions: {
          stackBars: true,
          axisX: {
            showGrid: false,
            showLabel: false,
            offset: 0,
          },
          axisY: {
            low: 0,
            showGrid: false,
            showLabel: false,
            offset: 0,
            labelInterpolationFnc: function (value) {
              return value / 1000 + 'k';
            },
          },
        },
        eventHandlers: [
          {
            event: 'draw',
            fn(data) {
              if (data.type === 'bar') {
                data.element.attr({
                  style: 'stroke-width: 3px',
                });
              }
            },
          },
        ],
      },
      smallchart4: {
        chartData_1: {
          labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
          series: [
            [400, 600, 800, 1000, 700, 1100, 300],
            [1000, 500, 600, 300, 700, 200, 1100],
          ],
        },
        chartOptions: {
          stackBars: true,
          axisX: {
            showGrid: false,
            showLabel: false,
            offset: 0,
          },
          axisY: {
            low: 0,
            showGrid: false,
            showLabel: false,
            offset: 0,
            labelInterpolationFnc: function (value) {
              return value / 1000 + 'k';
            },
          },
        },
        eventHandlers: [
          {
            event: 'draw',
            fn(data) {
              if (data.type === 'bar') {
                data.element.attr({
                  style: 'stroke-width: 3px',
                });
              }
            },
          },
        ],
      },
      apexDashboard: {
        options: {
          chart: {
            width: 685,
            height: 240,
            type: 'area',
            toolbar: {
              show: false,
            },
          },
          colors: [primary, secondary],
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
          },
          xaxis: {
            type: 'category',
            low: 0,
            offsetX: 0,
            offsetY: 0,
            show: false,
            categories: [
            ],
            labels: {
              low: 0,
              offsetX: 0,
              show: false,
            },
            axisBorder: {
              low: 0,
              offsetX: 0,
              show: false,
            },
          },
          yaxis: {
            low: 0,
            offsetX: 0,
            offsetY: 0,
            show: false,
            labels: {
              low: 0,
              offsetX: 0,
              show: false,
            },
            axisBorder: {
              low: 0,
              offsetX: 0,
              show: false,
            },
          },
          markers: {
            strokeWidth: 3,
            colors: '#ffffff',
            strokeColors: [ primary , secondary ],
            hover: {
              size: 6,
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.7,
              opacityTo: 0.5,
              stops: [0, 80, 100]
            }
          },
          legend: {
            show: false,
          },
          tooltip: {
            x: {
              format: 'MM'
            },
          },
          grid: {
            show: false,
            padding: {
              left: 0,
              right: 0,
              bottom: -15,
              top: -40
            }
          },
        },
        series: [
        ],
      },
      usersChart: {
        options: {
          chart: {
            width: 685,
            height: 240,
            type: 'area',
            toolbar: {
              show: false,
            },
          },
          colors: [primary, secondary],
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
          },
          xaxis: {
            type: 'category',
            low: 0,
            offsetX: 0,
            offsetY: 0,
            show: false,
            categories: [
            ],
            labels: {
              low: 0,
              offsetX: 0,
              show: false,
            },
            axisBorder: {
              low: 0,
              offsetX: 0,
              show: false,
            },
          },
          yaxis: {
            low: 0,
            offsetX: 0,
            offsetY: 0,
            show: false,
            labels: {
              low: 0,
              offsetX: 0,
              show: false,
            },
            axisBorder: {
              low: 0,
              offsetX: 0,
              show: false,
            },
          },
          markers: {
            strokeWidth: 3,
            colors: '#ffffff',
            strokeColors: [ primary , secondary ],
            hover: {
              size: 6,
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.7,
              opacityTo: 0.5,
              stops: [0, 80, 100]
            }
          },
          legend: {
            show: false,
          },
          tooltip: {
            x: {
              format: 'MM'
            },
          },
          grid: {
            show: false,
            padding: {
              left: 0,
              right: 0,
              bottom: -15,
              top: -40
            }
          },
        },
        series: [
        ],
      },
      apexMarketValue: {
        options: {
          chart: {
            width: 505,
            height: 380,
            type: 'radar',
            toolbar: {
              show: false,
            },
          },
          colors: [primary],
          dataLabels: {
            enabled: false,
          },
          labels: [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
          ],
          stroke: {
            width: 3,
            curve: 'smooth',
          },
          plotOptions: {
            radar: {
              size: 140,
              polygons: {
                fill: {
                  colors: ['#fcf8ff', '#f7eeff'],
                },
              },
            },
          },
          markers: {
            size: 6,
            colors: ['#fff'],
            strokeColor: [primary],
            strokeWidth: 3,
          },
          yaxis: {
            tickAmount: 7,
            labels: {
              formatter: function (val, i) {
                if (i % 2 === 0) {
                  return val;
                } else {
                  return '';
                }
              },
            },
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return val;
              },
            },
          },
        },
        series: [
          {
            name: 'Market value',
            data: [20, 100, 40, 30, 50, 80, 33],
          },
        ],
      },
      greeting : '',
      time : '',
      txBreakdowns: [],
      walletBreakdowns: [],
      stats: {},
    };
  },

  mounted() {
    var d = new Date();
    var curHr = this.addZero(d.getHours());
    var curMi = this.addZero(d.getMinutes());
    var meridiem = curHr >= 12 ? 'PM' : 'AM';
    this.time = curHr + ':' + curMi + ' ' + meridiem;
    if (curHr < 12) {
      this.greeting = 'Good morning!';
    }else if (curHr < 18) {
      this.greeting = 'Good afternoon!';
    }else {
      this.greeting = 'Good evening!';
    }
  },
  watch: {
    selectedOrg: {
      handler: async function () {
        if (!this.selectedOrg) {
          return
        }
        this.txBreakdowns = await this.tokenCheck.getTxBreakdowns(this.selectedOrg.id);
        this.walletBreakdowns = await this.tokenCheck.getWalletBreakdowns(this.selectedOrg.id);
        this.stats = await this.tokenCheck.getStats(this.selectedOrg.id);
      },
      deep: true,
      immediate: true,
    },
  },
  async created() {

  },
  computed: {
    tokenCheck() {
      return this.$store.state.user.tokenCheck;
    }
  },
  methods : {
    addZero(i) {
      if (i < 10) {
        i = '0' + i;
      }
      return i;
    }
  },
};
</script>
