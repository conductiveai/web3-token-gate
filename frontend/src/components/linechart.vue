<template>
  <div>
    <div class="col-xl-9 p-0">
      <div class="chart-right">
        <div class="row m-0 p-tb">
          <h5>{{ title }}</h5>
          <!--          <div class="col-xl-4 col-md-4 col-sm-4 col-12 p-0 justify-content-end">-->
          <!--            <div class="inner-top-right">-->
          <!--              <ul class="d-flex list-unstyled justify-content-end">-->
          <!--                <li v-for="breakdown in aggregatedBreakdown" :key="breakdown.name">{{ breakdown.name }}</li>-->
          <!--              </ul>-->
          <!--            </div>-->
          <!--          </div>-->
        </div>
        <div class="row">
          <div class="col-xl-12">
            <div class="card-body p-0">
              <div class="current-sale-container">
                <div id="chart-currently">
                  <apexchart
                      ref="apexTransactionBreakdown"
                      height="290"
                      type="area"
                      :options="apexDashboard.options"
                      :series="apexDashboard.series"
                  ></apexchart>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row border-top m-0">
        <div v-for="entry in aggregatedBreakdown" style="margin-top: 0!important;" class="col-xl-4 pl-0 col-md-6 col-sm-6">
          <div class="media p-0">
            <div class="media-left">
              <i class="icofont icofont-crown"></i>
            </div>
            <div class="media-body" :title="entry.name">
              <h6 class="text-ellipsis-100px">{{ entry.name }}</h6>
              <p class="text-ellipsis-100px"> {{ entry.value }} </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const primary = localStorage.getItem('primary_color') || '#7366ff';
const secondary = localStorage.getItem('secondary_color') || '#f73164';

export default {
  name: "LineChart",
  props: [
    'breakdowns',
    'title'
  ],
  computed: {
    aggregatedBreakdown() {
      return this.breakdowns.map((entry) => {
        return {
          name: entry.key,
          value: entry.items.reduce((acc, curr) => acc + curr.count, 0)
        }
      })
    }
  },
  created() {
  },
  watch: {
    breakdowns: {
      handler: function () {
        const categories = [];

        if (this.breakdowns.length > 0) {
          for (let entity of this.breakdowns[0].items) {
            categories.push(entity.label);
          }
        }

        this.apexDashboard.options = {
          ...this.apexDashboard.options,
          xaxis: {
            ...this.apexDashboard.options.xaxis,
            categories: categories
          }
        }

        const seriesData = [];
        for (const {key, items} of this.breakdowns) {
          seriesData.push({
            name: key,
            data: items.map(x => x.count)
          });
        }
        this.apexDashboard.series = seriesData;
      },
      deep: true,
    }
  },
  data() {
    return {
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
    }
  }
}
</script>

<style scoped>
.text-ellipsis-100px {
  text-overflow: ellipsis;
  overflow: hidden;
  width: 150px;
  white-space: nowrap;
}
</style>