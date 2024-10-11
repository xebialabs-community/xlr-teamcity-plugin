/*
 * Copyright 2024 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
window.addEventListener("xlrelease.load", function() {
  window.xlrelease.queryTileData(function(response) {
    const chart = echarts.init(document.getElementById("main"));
    const statuses = ["SUCCESS", "FAILURE"];
    let rawData = response.data.data.builds;

    function getMinutes(seconds) {
      return dayjs.utc(seconds).format("HH:mm:ss");
    }

    function getBarColor(status) {
      switch (status) {
        case "FAILURE":
          return "#93032E";
        case "SUCCESS":
          return "green";
        default:
          return "grey";
      }
    }

    function filterDataByStatus(status) {
      if (statuses.includes(status)) {
        statuses.splice(statuses.indexOf(status), 1);
      } else {
        statuses.push(status);
      }

      chart.setOption(getChartOptions());
    }

    function addLegendItemEventListener(item, status) {
      item.addEventListener("click", () => {
        filterDataByStatus(status);
        const icon = item.querySelector(".icon");
        const text = item.querySelector(".text");
        if (statuses.includes(status)) {
          icon.style.backgroundColor = getBarColor(status);
          text.style.color = "black";
        } else {
          icon.style.backgroundColor = "grey";
          text.style.color = "grey";
        }
      });
    }

    function drawLegend() {
      const legendEl = document.querySelector(".legend");
      Object.values(statuses).forEach((status) => {
        const legendItem = document.createElement("div");
        const legendIcon = document.createElement("div");
        const legendText = document.createElement("div");
        legendItem.classList.add("legend-item");
        legendIcon.classList.add("icon");
        legendText.classList.add("text");
        legendText.innerHTML = `<span>${status}</span>`;
        legendIcon.style.backgroundColor = getBarColor(status);
        legendItem.appendChild(legendIcon);
        legendItem.appendChild(legendText);
        addLegendItemEventListener(legendItem, status);
        legendEl.appendChild(legendItem);
      });
    }

    // construct chart options
    function getChartOptions() {
      return {
        title: {
          subtextStyle: {
            fontSize: "18",
            color: "black",
          },
          left: "center",
        },
        tooltip: {
          formatter: function (params) {
            const { value, id, status } = params.data;
            return `Build ID: ${id} <br>
                      Duration: ${getMinutes(value)} <br>
                      Result: ${status}`;
          },
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: function (value) {
              return getMinutes(value);
            },
          },
          name: "Build Time"
        },
        xAxis: {
          type: "category",
          label: {
            show: true,
            position: "insideRight",
          },
        },
        color: ["#52489C", "grey"],
        series: constructData(),
        legend: {
          data: ["Queue To Start", "Start To Finish"],
          icon: 'roundRect',
          itemGap: 32,
          textStyle: {
            fontSize: "16",
          },
        },
      };
    }

    // Structure data
    function constructData() {
      let firstBar = [];
      let secondBar = [];

      rawData.build
        .filter((build) => statuses.includes(build.status))
        .map(({ id, startDate, queuedDate, finishDate, status, webUrl }) => {
          const start = dayjs.utc(startDate);
          const queued = dayjs.utc(queuedDate);
          const finish = dayjs.utc(finishDate);
          const queueToStart = start.diff(queued, "ms");
          const startToFinish = finish.diff(start, "ms");
          const color = getBarColor(status);

          firstBar.push({
            id,
            value: queueToStart,
            status,
            webUrl,
            itemStyle: { color: "#52489C" },
          });

          secondBar.push({
            id,
            value: startToFinish,
            status,
            webUrl,
            itemStyle: { color },
          });
        });

      return [
        {
          name: "Queue To Start",
          barMinHeight: 10,
          type: "bar",
          data: firstBar,
          stack: "true",
        },
        {
          name: "Start To Finish",
          barMinHeight: 10,
          type: "bar",
          data: secondBar,
          stack: "true",
        },
      ];
    }

    // Interactions
    dayjs.extend(window.dayjs_plugin_utc);
    chart.setOption(getChartOptions());
    window.addEventListener("resize", () => chart.resize());
    chart.on("click", function (params) {
      if (params.data.webUrl) {
        window.open(params.data.webUrl, "_blank");
      }
    });
    drawLegend();
  })
})
