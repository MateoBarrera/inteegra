
var _table_ = document.createElement('table'),
  _tr_ = document.createElement('tr'),
  _th_ = document.createElement('th'),
  _td_ = document.createElement('td'),
  _thead_ = document.createElement('thead'),
  _tbody_ = document.createElement('tbody');

function  loadTable(arr){

  var table = _table_.cloneNode(false);
  var tbody = _tbody_.cloneNode(false),
    columns = addAllColumnHeaders(arr, table);
  for (var i = 0, maxi = arr.length; i < maxi; ++i) {
    var tr = _tr_.cloneNode(false);
    for (var j = 0, maxj = columns.length; j < maxj; ++j) {
      var th = _th_.cloneNode(false);
      cellValue = arr[i][columns[j]];
      th.appendChild(document.createTextNode(arr[i][columns[j]] || ''));
      /* console.log("Click" + th.textContent) */
      tr.appendChild(th);
    }   
    tbody.appendChild(tr);
  }
  table.appendChild(tbody);
  
  table.id = "table_info"
  table.classList.add("table");
  table.classList.add("table-hover");
  table.classList.add("text-secondary");

  function addAllColumnHeaders(arr, table) {
    var columnSet = [],
      thead = _thead_.cloneNode(false);
      tr = _tr_.cloneNode(false);
    for (var i = 0, l = arr.length; i < l; i++) {
      for (var key in arr[i]) {
        if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) {
          columnSet.push(key);
          var th = _th_.cloneNode(false);
          th.appendChild(document.createTextNode(key));
          tr.appendChild(th);
        }
      }
    }
    thead.appendChild(tr);
    thead.classList.add("text-primary");
    table.appendChild(thead);
    return columnSet;
  }

  var el = document.getElementById("table_content");
  el.innerHTML= "";
  el.appendChild(table);
  const datatablesSimple = document.getElementById('table_info');
  if (datatablesSimple) {
    let tables = new DataTable(datatablesSimple, {
    language: {
      url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'
    }, responsive:true});
  }

  var table_handler = $('#table_info').DataTable();
  $('#table_info tbody').on('click', 'tr', function () {
    console.log("Se esta ejecutando.....")
    var data = table_handler.row(this).data(); 
    var data = table_handler.column().header();
    alert( 'You clicked on '+$(data).html()+'\'s row' );
} );
}



[
	{
		idsesiones: 84,
		nombre: "Mateo Barrera",
		estudiante: "Estudiante Prueba",
		fecha: "2022-03-24",
		hora: "23:50:35",
	},
	{
		idsesiones: 94,
		nombre: "Mateo Barrera",
		estudiante: "Estudiante Prueba",
		fecha: "2022-03-25",
		hora: "08:30:33",
	},
	{
		idsesiones: 104,
		nombre: "Mateo Barrera",
		estudiante: "Estudiante Prueba",
		fecha: "2022-03-25",
		hora: "19:27:53",
	},
	{
		idsesiones: 114,
		nombre: "Nancy Paredes",
		estudiante: "Estudiante Prueba",
		fecha: "2022-03-25",
		hora: "22:41:01",
	},
	{
		idsesiones: 124,
		nombre: "Nancy Paredes",
		estudiante: "Estudiante Prueba",
		fecha: "2022-03-25",
		hora: "22:43:18",
	},
	{
		idsesiones: 134,
		nombre: "Mateo Barrera",
		estudiante: "Univalluno",
		fecha: "2022-04-04",
		hora: "18:02:36",
	},
	{
		idsesiones: 144,
		nombre: "Mateo Barrera",
		estudiante: "Univalluno",
		fecha: "2022-04-04",
		hora: "18:09:17",
	},
	{
		idsesiones: 154,
		nombre: "Mateo Barrera",
		estudiante: "Univalluno",
		fecha: "2022-04-04",
		hora: "18:30:51",
	},
]