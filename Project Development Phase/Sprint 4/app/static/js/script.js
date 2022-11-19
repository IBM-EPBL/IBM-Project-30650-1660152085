const ctx = document.getElementById("graph");

function daysInThisMonth() {
  var now = new Date();
  return new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
}

const days = Array(daysInThisMonth())
  .fill()
  .map((_, idx) => 1 + idx);
console.log(days)

new Chart(ctx, {
  type: "bar",
  data: {
    labels: days,
    datasets: [
      {
        label: "Income",
        data: [30, 40, 2, 2, 33, 23],
        borderWidth: 1,
      },
      {
        label: "Expenses",
        data: [20, 10, 3, 50, 20, 3],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
