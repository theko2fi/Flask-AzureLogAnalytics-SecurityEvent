new gridjs.Grid({
    columns: ["DateGenerated","TimeGenerated", "Activity", "AccountName"],
    search: true,
    sort: true,
    server: {
        url: '/data',
        then: data => data.tables[0].rows
    } 
  }).render(document.getElementById("wrapper"));