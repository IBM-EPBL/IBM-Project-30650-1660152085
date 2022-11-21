const ctx = document.getElementById("graph");

function daysInThisMonth() {
  var now = new Date();
  return new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
}


const income = []
const expense = []

for(let i=1;i<daysInThisMonth();i++){
  let inc = 0
  let exp = 0
  data.transaction.forEach(transaction => {
    if(new Date(transaction.time).getDate() == i){
      if(transaction.type == "Income"){
        inc += transaction.amount;
      }else{
        exp += transaction.amount;
      }
      
    }
  });
  income.push(inc)
  expense.push(exp)
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
        data: income,
        borderWidth: 1,
      },
      {
        label: "Expenses",
        data: expense,
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
