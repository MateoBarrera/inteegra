var last_indicator_3 = ""
var chart_element_3 = ""
var keys_list_3 = []
var last_indicator_4 = ""
var chart_element_4 = ""
var keys_list_4 = []
var last_indicator_5 = ""
var chart_element_5 = ""
var keys_list_5 = []
var last_indicator_6 = ""
var chart_element_6 = ""
var keys_list_6 = []
var last_indicator_7 = ""
var chart_element_7 = ""
var keys_list_7 = []
var last_indicator_8 = ""
var chart_element_8 = ""
var keys_list_8 = []
let data_topsis = []
var strategies_const
let const_strategies = {}
let const_loss_factor = {}
let data_for_topsis_dist = []
var al = Math.floor(Math.random() * 255)
var b_colorslist = [
    "rgba(" + al + ", 99, 132, 0.8)",
    "rgba(" + al + ", 162, 235, 0.8)",
    "rgba(" + al + ", 206, 86, 0.8)",
    "rgba(" + al + ", 192, 192, 0.8)",
    "rgba(" + al + ", 102, 255, 0.8)",
    "rgba(" + al + ", 159, 64, 0.8)",
]
var colorslist = [
    "rgba(" + al + ", 99, 132, 1)",
    "rgba(" + al + ", 162, 235, 1)",
    "rgba(" + al + ", 206, 86, 1)",
    "rgba(" + al + ", 192, 192, 1)",
    "rgba(" + al + ", 102, 255, 1)",
    "rgba(" + al + ", 159, 64, 1)",
]

var units_array = []
var for_save_indicators= []
var for_save_generation= []
var for_save_consumption= []
var id_edit

function loadUnit(units) {
    units_array = units
}

function validateDate() {
    let anio_base = 2021
    let year_selected = parseInt(document.getElementById("fecha").innerText)
    let n = year_selected - anio_base
    return [n, year_selected]
}

document.getElementById("adjust_sub_estrategies_prev").addEventListener("click", function () {
    cleanGrahpVariables()
})

document.getElementById("visalization_indicators_prev").addEventListener("click", function () {
    cleanGrahpIndicators()
})

document.getElementById("visalization_topsis_prev").addEventListener("click", function () {
    cleanGrahpTopsis()
})

document.getElementById("guardar").addEventListener("click", function () {
    saveDataStrategy(strategies_const);
})

document.getElementById("guardar_editado").addEventListener("click", function () {
    editDataStrategy(strategies_const,id_edit)
})

function cleanGrahpVariables() {
    if (chart_element_3) {
        chart_element_3.destroy()
        document.getElementById("chart_title_3").innerHTML = " "
    }
    if (chart_element_4) {
        chart_element_4.destroy()
        document.getElementById("chart_title_4").innerHTML = " "
    }
}

function cleanGrahpIndicators() {
    if (chart_element_5) {
        chart_element_5.destroy()
        document.getElementById("chart_title_5").innerHTML = " "
    }
    if (chart_element_6) {
        chart_element_6.destroy()
        document.getElementById("chart_title_6").innerHTML = " "
    }
    if (chart_element_7) {
        chart_element_7.destroy()
        document.getElementById("chart_title_7").innerHTML = " "
    }
    for_save_generation=[]
    for_save_consumption = []
    for_save_indicators = []
}

function cleanGrahpTopsis() {
    if (chart_element_8) {
        chart_element_8.destroy()
        document.getElementById("chart_title_8").innerHTML = " "
    }
}

function checkParameters() {
    var year_selected = document.getElementById("fecha").innerText
    var text_process_selected = $("#process-selected").find("span").text()
    var name_scenario = document.getElementById("name-input").value
    if (
        !(year_selected === "Seleccionar") &&
        !(text_process_selected === "Seleccionar") &&
        !(name_scenario == null)
    ) {
        loadParameters(name_scenario, text_process_selected, year_selected)
        ActiveSection("scenarios_2")
        return
    } else {
        $("#error-section").text("Verifique los campos ingresados")
        if (year_selected === "Seleccionar") {
            $("#select-year").addClass("btn-danger")
        }
        if (text_process_selected === "Seleccionar") {
            $("#process-selected").addClass("btn-danger")
        }
        if (!name_scenario) {
            $("#name-input").addClass("border-danger")
        }
    }
}

function loadParameters(name, process, year_selected) {
    document.querySelectorAll("#scenario-name-macro").forEach(function (element) {
        element.innerHTML = name
    })
    document.querySelectorAll("#scenario-process-macro").forEach(function (element) {
        element.innerHTML = process
    })
    document.querySelectorAll("#scenario-anio-macro").forEach(function (element) {
        element.innerHTML = year_selected
    })
}

function createChartExpansion(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return parseFloat((x * 100).toFixed(3))
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_3.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_3.includes(row_table) && graphAlreadyExist) {
            keys_list_3.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_3.length],
                backgroundColor: b_colorslist[keys_list_3.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_3.data.datasets.push(update_dataset)
            chart_element_3.update()
            return
        } else {
            {
                keys_list_3 = [row_table]
                var mydatasets = [
                    {
                        label: row_table,
                        borderColor: colorslist[0],
                        backgroundColor: b_colorslist[0],
                        borderWidth: 2,
                        data: array,
                        spanGraphs: false,
                        fill: true,
                    },
                ]
                let delayed
                $("#" + line_chart).remove()
                $("#" + graph_container).append(
                    '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
                )
                var config = {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: mydatasets,
                    },
                    options: {
                        responsive: true,
                        scales: {
                            xAxes: [
                                {
                                    stacked: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Año",
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    stacked: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: unit,
                                    },
                                },
                            ],
                        },
                        title: {
                            display: false,
                            text: table_name,
                        },
                        legend: {
                            position: "bottom",
                        },
                        animation: {
                            onComplete: () => {
                                delayed = true
                            },
                            delay: (context) => {
                                let delay = 0
                                if (context.type === "data" && context.mode === "default" && !delayed) {
                                    delay = context.dataIndex * 300 + context.datasetIndex * 100
                                }
                                return delay
                            },
                        },
                    },
                }
                chart_element_3 = new Chart(document.getElementById(line_chart), config)
            }
            last_indicator_3 = indicator
        }
    }
}

function createChartUpgrade(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return parseFloat((x * 100).toFixed(3))
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_4.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_4.includes(row_table) && graphAlreadyExist) {
            keys_list_4.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_4.length],
                backgroundColor: b_colorslist[keys_list_4.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_4.data.datasets.push(update_dataset)
            chart_element_4.update()
        } else {
            keys_list_4 = [row_table]
            var mydatasets = [
                {
                    label: row_table,
                    borderColor: colorslist[0],
                    backgroundColor: b_colorslist[0],
                    borderWidth: 2,
                    data: array,
                    spanGraphs: false,
                    fill: true,
                },
            ]
            let delayed
            $("#" + line_chart).remove()
            $("#" + graph_container).append(
                '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
            )
            var config = {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: mydatasets,
                },
                options: {
                    responsive: true,
                    scales: {
                        xAxes: [
                            {
                                stacked: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: "Año",
                                },
                            },
                        ],
                        yAxes: [
                            {
                                stacked: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: unit,
                                },
                            },
                        ],
                    },
                    title: {
                        display: false,
                        text: table_name,
                    },
                    legend: {
                        position: "bottom",
                    },
                    animation: {
                        onComplete: () => {
                            delayed = true
                        },
                        delay: (context) => {
                            let delay = 0
                            if (context.type === "data" && context.mode === "default" && !delayed) {
                                delay = context.dataIndex * 300 + context.datasetIndex * 100
                            }
                            return delay
                        },
                    },
                },
            }
            chart_element_4 = new Chart(document.getElementById(line_chart), config)
        }
        last_indicator_4 = indicator
    }
}

function createChartIndicador1(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return parseFloat((x * 100).toFixed(3))
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_5.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_5.includes(row_table) && graphAlreadyExist) {
            keys_list_5.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_5.length],
                backgroundColor: b_colorslist[keys_list_5.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_5.data.datasets.push(update_dataset)
            chart_element_5.update()
            return
        } else {
            {
                keys_list_5 = [row_table]
                var mydatasets = [
                    {
                        label: row_table,
                        borderColor: colorslist[0],
                        backgroundColor: b_colorslist[0],
                        borderWidth: 2,
                        data: array,
                        spanGraphs: false,
                        fill: true,
                    },
                ]
                let delayed
                $("#" + line_chart).remove()
                $("#" + graph_container).append(
                    '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
                )
                var config = {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: mydatasets,
                    },
                    options: {
                        responsive: true,
                        scales: {
                            xAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Año",
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: unit,
                                    },
                                },
                            ],
                        },
                        title: {
                            display: false,
                            text: table_name,
                        },
                        legend: {
                            position: "bottom",
                        },
                        animation: {
                            onComplete: () => {
                                delayed = true
                            },
                            delay: (context) => {
                                let delay = 0
                                if (context.type === "data" && context.mode === "default" && !delayed) {
                                    delay = context.dataIndex * 300 + context.datasetIndex * 100
                                }
                                return delay
                            },
                        },
                    },
                }
                chart_element_5 = new Chart(document.getElementById(line_chart), config)
            }
            last_indicator_5 = indicator
        }
    }
}

function createChartIndicador2(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return parseFloat((x * 100).toFixed(3))
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_6.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_6.includes(row_table) && graphAlreadyExist) {
            keys_list_6.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_6.length],
                backgroundColor: b_colorslist[keys_list_6.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_6.data.datasets.push(update_dataset)
            chart_element_6.update()
            return
        } else {
            {
                keys_list_6 = [row_table]
                var mydatasets = [
                    {
                        label: row_table,
                        borderColor: colorslist[0],
                        backgroundColor: b_colorslist[0],
                        borderWidth: 2,
                        data: array,
                        spanGraphs: false,
                        fill: true,
                    },
                ]
                let delayed
                $("#" + line_chart).remove()
                $("#" + graph_container).append(
                    '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
                )
                var config = {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: mydatasets,
                    },
                    options: {
                        responsive: true,
                        scales: {
                            xAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Año",
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: unit,
                                    },
                                },
                            ],
                        },
                        title: {
                            display: false,
                            text: table_name,
                        },
                        legend: {
                            position: "bottom",
                        },
                        animation: {
                            onComplete: () => {
                                delayed = true
                            },
                            delay: (context) => {
                                let delay = 0
                                if (context.type === "data" && context.mode === "default" && !delayed) {
                                    delay = context.dataIndex * 300 + context.datasetIndex * 100
                                }
                                return delay
                            },
                        },
                    },
                }
                chart_element_6 = new Chart(document.getElementById(line_chart), config)
            }
            last_indicator_6 = indicator
        }
    }
}

function createChartIndicador3(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return parseFloat((x * 100).toFixed(3))
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_7.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_7.includes(row_table) && graphAlreadyExist) {
            keys_list_7.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_7.length],
                backgroundColor: b_colorslist[keys_list_7.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_7.data.datasets.push(update_dataset)
            chart_element_7.update()
            return
        } else {
            {
                keys_list_7 = [row_table]
                var mydatasets = [
                    {
                        label: row_table,
                        borderColor: colorslist[0],
                        backgroundColor: b_colorslist[0],
                        borderWidth: 2,
                        data: array,
                        spanGraphs: false,
                        fill: true,
                    },
                ]
                let delayed
                $("#" + line_chart).remove()
                $("#" + graph_container).append(
                    '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
                )
                var config = {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: mydatasets,
                    },
                    options: {
                        responsive: true,
                        scales: {
                            xAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Año",
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: unit,
                                    },
                                },
                            ],
                        },
                        title: {
                            display: false,
                            text: table_name,
                        },
                        legend: {
                            position: "bottom",
                        },
                        animation: {
                            onComplete: () => {
                                delayed = true
                            },
                            delay: (context) => {
                                let delay = 0
                                if (context.type === "data" && context.mode === "default" && !delayed) {
                                    delay = context.dataIndex * 300 + context.datasetIndex * 100
                                }
                                return delay
                            },
                        },
                    },
                }
                chart_element_7 = new Chart(document.getElementById(line_chart), config)
            }
            last_indicator_7 = indicator
        }
    }
}

function createChartTopsis(
    list_name,
    indicator,
    key,
    dataModel_pruebas_expansion,
    chart_title,
    line_chart,
    graph_container
) {
    var row = key
    var row_table = row

    const table_name = indicator
    document.getElementById(chart_title).innerHTML = table_name
    var json_file = dataModel_pruebas_expansion
    var table = json_file[table_name]
    var keys = Object.keys(table[0])
    var labels = table.map(function (e) {
        return e[keys[0]]
    })
    labels = labels.slice(0, 12)
    var data = table.map(function (e) {
        return e[row]
    })
    length = data.length
    var array = []
    for (var j = 0; j < length; j++) {
        array.push(parseFloat(data[j].toFixed(3)))
    }
    var unit = ""
    var units = units_array
    if (indicator in units) {
        unit = units[indicator]
        if (unit == "Porcentaje %") {
            array = array.map(function (x) {
                return x * 100
            })
        }
    }
    /* Agregada - Capturar graficas actuales > 2 restablece */
    /* Desagregados - else */
    try {
        _ = chart_element_8.data.datasets
        var graphAlreadyExist = true
    } catch (e) {
        var graphAlreadyExist = false
    } finally {
        if (!keys_list_8.includes(row_table) && graphAlreadyExist) {
            keys_list_8.push(row_table)
            const update_dataset = {
                label: row_table,
                borderColor: colorslist[keys_list_8.length],
                backgroundColor: b_colorslist[keys_list_8.length],
                borderWidth: 2,
                data: array,
                spanGraphs: false,
                fill: true,
            }
            chart_element_8.data.datasets.push(update_dataset)
            chart_element_8.update()
            return
        } else {
            {
                keys_list_8 = [row_table]
                var mydatasets = [
                    {
                        label: row_table,
                        borderColor: colorslist[0],
                        backgroundColor: b_colorslist[0],
                        borderWidth: 2,
                        data: array,
                        spanGraphs: false,
                        fill: true,
                    },
                ]
                let delayed
                $("#" + line_chart).remove()
                $("#" + graph_container).append(
                    '<canvas id="' + line_chart + '" width="100%" height="48vh"><canvas>'
                )
                var config = {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: mydatasets,
                    },
                    options: {
                        responsive: true,
                        scales: {
                            xAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: false,
                                        labelString: "Año",
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    stacked: false,
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Índice de dominancia",
                                    },
                                },
                            ],
                        },
                        title: {
                            display: false,
                            text: table_name,
                        },
                        legend: {
                            position: "bottom",
                        },
                        animation: {
                            onComplete: () => {
                                delayed = true
                            },
                            delay: (context) => {
                                let delay = 0
                                if (context.type === "data" && context.mode === "default" && !delayed) {
                                    delay = context.dataIndex * 300 + context.datasetIndex * 100
                                }
                                return delay
                            },
                        },
                    },
                }
                chart_element_8 = new Chart(document.getElementById(line_chart), config)
            }
            last_indicator_8 = indicator
        }
    }
}

function loadSliders(strategies_array) {
    $(".form-range").each(function () {
        $(this).bootstrapSlider()
        $(this).on("change", {passive: true}, function (slideEvt) {
            $(this).parents(".group-form-range").find(".form-range-value").text(slideEvt.value.newValue)
        })
        $(this).on("slideStop", {passive: true}, function (slideEvt) {
            slideEvt.preventDefault()
            updateChart(strategies_array)
        })
    })
    addClass()
    /* test de render whit js */
}

function loadInputsAux(strategies_array) {
    $(".form-control-sm").each(function () {
        $(this).on("change", {passive: true}, function (slideEvt) {
            slideEvt.preventDefault()
            updateChart(strategies_array)
        })
    })
}

function removeSliders() {
    const boxes = document.querySelectorAll(".slider")
    boxes.forEach((box) => {
        box.remove()
    })
}

function addClass() {
    document.getElementsByClassName("slider").forEach((element) => {
        element.classList.add("slider-volt")
    })
}

function getProcessName() {
    var processName = $("#process-selected").find("span").text()
    if (processName == "Generación") {
        processName = "generation"
    } else if (processName == "Distribución") {
        processName = "distribution"
    } else if (processName == "Uso final") {
        processName = "end_use"
    }
    return processName
}

function loadModel(model, parent) {
    var model_html = parent.querySelector("#accordion-item-model-id").cloneNode(true)
    model_html.id = "accordion-item-model-" + model.id
    model_html.querySelector("#model-name").innerHTML = model.name
    model_html.querySelector("#heading-model-id").id = "heading-model-" + model.id
    model_html
        .querySelector(".accordion-button")
        .setAttribute("data-bs-target", "#collapse-model-" + model.id)
    model_html
        .querySelector(".accordion-button")
        .setAttribute("aria-controls", "collapse-model-" + model.id)
    model_html
        .querySelector("#collapse-model-id")
        .setAttribute("aria-labelledby", "heading-model-" + model.id)
    model_html.querySelector("#collapse-model-id").id = "collapse-model-" + model.id
    return model_html
}

function toggleAuxInput(input_name) {
    document.getElementById(input_name).toggleAttribute("disabled")
}

function loadAuxVariable(strategy) {
    var variable_aux_html = document.querySelector("#strategy-variable-aux-example").cloneNode(true)
    variable_aux_html.querySelector("#variable-aux-name-strategy").innerText = strategy.variable_aux
    variable_aux_html.querySelector("#variable-aux-name-strategy").id =
        "variable-aux-name-strategy-" + strategy.id
    variable_aux_html
        .querySelector("#aux-input-strategy")
        .setAttribute("min", String(strategy.lower_value_aux))
    variable_aux_html
        .querySelector("#aux-input-strategy")
        .setAttribute("max", String(strategy.upper_value_aux))
    variable_aux_html
        .querySelector("#aux-input-strategy")
        .setAttribute("value", String(strategy.value_aux))
    variable_aux_html.querySelector("#range-aux-info-strategy").innerText =
        strategy.lower_value_aux + "-" + strategy.upper_value_aux + " " + strategy.unit_aux

    let name_aux_input = "aux-input-strategy-" + strategy.id
    variable_aux_html
        .querySelector("#variable-aux-checker")
        .setAttribute("onclick", "toggleAuxInput('" + name_aux_input + "')")

    variable_aux_html.querySelector("#aux-input-strategy").id = name_aux_input

    return variable_aux_html
}

function loadStrategy(strategy, parent, idModel) {
    var strategy_html = parent.querySelector("#strategy-item-example").cloneNode(true)
    strategy_html.id = "accordion-strategy-" + strategy.id
    strategy_html.querySelector("#strategy-example-name").innerHTML = strategy.name
    strategy_html.querySelector("#strategy-example-name").id = "strategy-" + strategy.id + "-name"
    strategy_html.querySelector("#heading-strategy-example").id = "heading-strategy-" + strategy.id

    strategy_html
        .querySelector(".accordion-button")
        .setAttribute("data-bs-target", "#collapse-strategy-" + strategy.id)
    strategy_html
        .querySelector(".accordion-button")
        .setAttribute("aria-controls", "collapse-strategy-" + strategy.id)
    strategy_html
        .querySelector("#collapse-strategy-example")
        .setAttribute("aria-labelledby", "heading-strategy-" + strategy.id)
    strategy_html
        .querySelector("#collapse-strategy-example")
        .setAttribute("data-bs-parent", "#strategies-model-" + idModel)
    strategy_html.querySelector("#collapse-strategy-example").id = "collapse-strategy-" + strategy.id
    strategy_html.querySelector("#strategy-name-variable").innerHTML = strategy.variable
    strategy_html.querySelector(".form-range").setAttribute("data-slider-min", strategy.lower_value)
    strategy_html
        .querySelector(".form-range")
        .setAttribute("data-slider-max", String(strategy.upper_value))
    strategy_html
        .querySelector(".form-range")
        .setAttribute("data-slider-min", String(strategy.lower_value))
    strategy_html
        .querySelector(".form-range")
        .setAttribute("data-slider-value", String(strategy.value))
    strategy_html
        .querySelector(".form-range")
        .setAttribute("data-slider-id", "range-strategy-" + strategy.id)
    strategy_html.querySelector("#strategy-example-unit").innerHTML = strategy.unit
    strategy_html.querySelector("#strategy-bau-info").innerHTML =
        strategy.value + " " + strategy.unit + " " + strategy.year
    strategy_html.querySelector("#strategy-range-info").innerHTML =
        strategy.lower_value + "-" + strategy.upper_value + " " + strategy.unit
    strategy_html.querySelector("#strategy-example-current-value").innerHTML = strategy.value
    strategy_html.querySelector("#strategy-example-current-value").classList.add("form-range-value")
    strategy_html.querySelector("#strategy-example-current-value").id = "current-value-" + strategy.id

    if (strategy.variable_aux !== undefined) {
        var aux_html = loadAuxVariable(strategy)
        strategy_html.querySelector("#aux_var_section").appendChild(aux_html)
    }

    return strategy_html
}

function filterStrategiesByProcess(strategies_array) {
    let current_process = getProcessName()
    let new_strategies = Object.fromEntries(
        Object.entries(strategies_array).filter(([key]) => key.includes(current_process))
    )
    return new_strategies[current_process]
}

function filterStrategiesById(array, ids) {
    let n_and_year = validateDate()
    let n = n_and_year[0]
    let anio = n_and_year[1]
    let exist = false
    let exist_ = false
    if (array.process == "Uso final") {
        exist = true
    } else if (array.process == "Distribución") {
        exist_ = true
    }
    let new_array = array.models
        .filter((model) => model.strategies.some((strategy) => ids.includes(strategy.id)))
        .map((model) => {
            let newElt
            if (exist) {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue
                            if (typeof inStrategies.pi_bau !== "undefined") {
                                let new_value = (inStrategies.pi_bau[n - 1] * 100).toFixed(1)
                                newEltValue = Object.assign({}, inStrategies, {
                                    value: new_value,
                                    year: anio,
                                })
                            } else if (typeof inStrategies.num_vehic_elect !== "undefined") {
                                let new_value = Math.round(inStrategies.num_vehic_elect[n - 1])
                                newEltValue = Object.assign({}, inStrategies, {
                                    value: new_value,
                                    year: anio,
                                })
                            }
                            return newEltValue
                        }),
                })
            } else if (exist_) {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies.filter((strategy) => ids.includes(strategy.id)),
                })
                return newElt
            } else {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue
                            if (typeof inStrategies.values_CI !== "undefined") {
                                let new_value = Math.round(inStrategies.values_CI[n - 1])
                                newEltValue = Object.assign({}, inStrategies, {
                                    value: new_value,
                                    year: anio,
                                })
                            } else if (typeof inStrategies.efi_deseada_base !== "undefined") {
                                let new_value = Math.round(inStrategies.efi_deseada_base[n - 1])
                                newEltValue = Object.assign({}, inStrategies, {
                                    value: new_value,
                                    year: anio,
                                })
                            }
                            return newEltValue
                        }),
                })
            }
            return newElt
        })
    array.models = new_array
    return array
}

function filterStrategiesByIdRelationated(array, ids) {
    let new_array = array.models
        .filter((model) => model.strategies.some((strategy) => ids.includes(strategy.id_relation)))
        .map((model) => {
            let newElt = Object.assign({}, model, {
                strategies: model.strategies.filter((strategy) => ids.includes(strategy.id_relation)),
            })
            return newElt
        })
    array.models = new_array
    return array
}

function filterStrategiesByIdValues(array, idsValues, idsValuesText) {
    let ids = Object.keys(idsValues)
    let exist = false
    if (Object.keys(idsValuesText).length > 0) {
        exist = true
    }
    let new_array = array.models
        .filter((model) => model.strategies.some((strategy) => ids.includes(strategy.id)))
        .map((model) => {
            let newElt
            if (exist) {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue = Object.assign({}, inStrategies, {
                                selected_value: idsValues[ids.find((strategiId) => strategiId == inStrategies.id)],
                                selected_value_aux:
                                    idsValuesText[ids.find((strategiId) => strategiId == inStrategies.id)],
                            })
                            return newEltValue
                        }),
                })
            } else {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue = Object.assign({}, inStrategies, {
                                selected_value: idsValues[ids.find((strategiId) => strategiId == inStrategies.id)],
                            })
                            return newEltValue
                        }),
                })
            }
            return newElt
        })
    array.models = new_array
    return array
}

//let const_strategies = {}
function loadStrategies(strategies_array, strategies_id_selected) {
    const_strategies = JSON.parse(JSON.stringify(strategies_array))
    strategies_array = filterStrategiesByProcess(strategies_array)
    strategies_to_show = filterStrategiesById(strategies_array, strategies_id_selected)
    var parent = document.getElementById("template_strategies").cloneNode(true)
    parent.querySelector("#process").innerHTML = strategies_array.process
    strategies_array.models.forEach((model) => {
        var model_html = loadModel(model, parent)
        model.strategies.forEach((strategy) => {
            model_html
                .querySelector("#strategies-model-id")
                .appendChild(loadStrategy(strategy, model_html, model.id))
        })
        model_html.querySelector("#strategies-model-id").id = "strategies-model-" + model.id
        /* model_html.querySelector("#strategies-model-id").id = "strategies-model-" + model.id */
        parent.querySelector("#accordion-strategies").appendChild(model_html)
    })
    document.getElementById("test-clone").innerHTML = ""
    document.getElementById("test-clone").appendChild(parent)
    removeSliders()
    loadSliders(strategies_array)
    loadInputsAux(strategies_array)
    updateChart(strategies_array)
}

function getCurrentValues() {
    //console.log("getCurrentValues")
    let key_values = {}
    let text_values = {}
    document.querySelectorAll(".form-range-value").forEach(function (values) {
        key_id = String(values.id.split("-").slice(-1))
        value_slider = values.innerHTML
        var aux_input = document.querySelector("#aux-input-strategy-" + key_id)
        value_aux = null
        if (aux_input !== null) {
            //value_aux = aux_input.value
            value_aux = aux_input.hasAttribute("disabled") ? false : aux_input.value
            text_values[key_id] = value_aux
        }
        key_values[key_id] = value_slider
    })
    return [key_values, text_values]
}

function getStrategieName() {
    let strategieName = []
    strategieName.push("Estrategias de expansión")
    strategieName.push("Estrategias de actualización")
    return strategieName
}

// function getCurrentValuesIds() {
// 	let ids = []
// 	let values_sliders = []
// 	document.querySelectorAll(".form-range-value").forEach(function (values) {
// 		key_id = String(values.id.split("-").slice(-1))
// 		value_slider = values.innerHTML
// 		ids.push(key_id)
// 		values_sliders.push(value_slider)
// 	})
// 	return [ids, values_sliders]
// }
function generateGhapExpansion(sub_strategies, n, strategies_name) {
    let sub_strategies_key = Object.keys(sub_strategies)
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies[item].name
        let sub_strategies_value = parseFloat(sub_strategies[item].selected_value)
        let sub_strategies_fp = parseFloat(sub_strategies[item].fp)
        let sub_strategies_gen_historico = parseFloat(sub_strategies[item].generacion_historica)

        let data_model_expansion = modelExpansionEstrategy(
            n,
            sub_strategies_value,
            sub_strategies_fp,
            sub_strategies_name,
            sub_strategies_gen_historico
        )
        createChartExpansion(
            list_name,
            strategies_name,
            sub_strategies_name,
            data_model_expansion,
            "chart_title_3",
            "line-chart-3",
            "graph-container-3"
        )
    })
}

function generateGhapUpgrade(sub_strategies, n, strategies_name) {
    let sub_strategies_key = Object.keys(sub_strategies)
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies[item].name
        let sub_strategies_value = parseFloat(sub_strategies[item].selected_value) / 100
        let sub_strategies_n_LB = sub_strategies[item].n_LB
        let sub_strategies_data = sub_strategies[item].values_BAU
        let plot_upgrade = modelUpgradeStrategy(
            n,
            sub_strategies_value,
            sub_strategies_data,
            sub_strategies_n_LB,
            sub_strategies_name
        )
        createChartUpgrade(
            list_name,
            strategies_name,
            sub_strategies_name,
            plot_upgrade,
            "chart_title_4",
            "line-chart-4",
            "graph-container-4"
        )
    })
}

// funcion que recive un objeto tipo json 
// y devuelve el nombre y el valor 
// en dos arrays independientes

function modifyData(data) {
    let dataReturn = []
    let list_names = Object.keys(data)
    let name_return = ""
    list_names.forEach(function (item, index) {
        let data_loop = data[item]
        let data_loop_keys = Object.keys(data_loop)
        let name = Object.keys(data_loop[0])
        name_return = name[1]

        data_loop_keys.forEach(function (item2, index2) {
            let data_loop_keys_item = data[item][item2]
            let data_loop_keys2 = Object.values(data_loop_keys_item)
            dataReturn.push(data_loop_keys2[1])
        })
    })
    return [dataReturn, name_return]
}

function validateNameIndicatorEficiency(name) {
    if (name == "Generación eléctrica a partir de plantas térmicas") {
        name = "Eficiencia energética en plantas térmicas"
    } else if (name == "Generación eléctrica a partir de plantas hidráulicas") {
        name = "Eficiencia energética plantas hidráulicas"
    } else if (name == "Generación eléctrica a partir de plantas de Auto y Cogeneración") {
        name = "Eficiencia energética en plantas de Auto y Cogeneración"
    } else if (name == "Generación eléctrica a partir de plantas eólicas") {
        name = "Eficiencia en plantas eólicas"
    } else if (name == "Generación eléctrica a partir de plantas solares") {
        name = "Eficiencia en plantas solares"
    }
    return name
}

function validateNameIndicatorIep(name) {
    if (name == "Generación eléctrica a partir de plantas térmicas") {
        name = "Intensidad energética primaria en plantas térmicas"
    } else if (name == "Generación eléctrica a partir de plantas hidráulicas") {
        name = "Intensidad energética primaria en plantas hidráulicas"
    } else if (name == "Generación eléctrica a partir de plantas de Auto y Cogeneración") {
        name = "Intensidad energética primaria en plantas de Auto y Cogeneración"
    } else if (name == "Generación eléctrica a partir de plantas eólicas") {
        name = "Intensidad energética primaria en plantas eólicas"
    } else if (name == "Generación eléctrica a partir de plantas solares") {
        name = "Intensidad energética primaria en plantas solares"
    }
    return name
}

function validateNameIndicatorIec(name) {
    if (name == "Generación eléctrica a partir de plantas térmicas") {
        name = "Emisiones de carbono en plantas térmicas"
    } else if (name == "Generación eléctrica a partir de plantas hidráulicas") {
        name = "Emisiones de carbono en plantas hidráulicas"
    } else if (name == "Generación eléctrica a partir de plantas de Auto y Cogeneración") {
        name = "Emisiones de carbono en plantas de Auto y Cogeneración"
    } else if (name == "Generación eléctrica a partir de plantas eólicas") {
        name = "Emisiones de carbono en plantas eólicas"
    } else if (name == "Generación eléctrica a partir de plantas solares") {
        name = "Emisiones de carbono en plantas solares"
    }
    return name
}

function generationIndicatorEficiency(generacion, consumo, name) {
    name = validateNameIndicatorEficiency(name)
    let eficiency = 0
    let data_plot_eficiency = []
    let k = 2
    let anio_eficiency = ""
    let data_plot_return = []
    for (var i = 0; i < generacion.length; i++) {
        let data_plot_dict = {}
        anio_eficiency = "202" + k
        if (k > 9) {
            k = 0
            anio_eficiency = "203" + k
        }
        k++
        eficiency = generacion[i] / consumo[i]
        data_plot_dict.Año = anio_eficiency
        data_plot_dict[name] = eficiency
        data_plot_eficiency.push(data_plot_dict)
    }
    data_plot_return["Indicador de eficiencia energética"] = data_plot_eficiency
    createChartIndicador1(
        list_name,
        "Indicador de eficiencia energética",
        name,
        data_plot_return,
        "chart_title_5",
        "line-chart-5",
        "graph-container-5"
    )
    return data_plot_return
}

function generationIndicatorsIEP(consumo, pib, name) {
    // Generación con recurso hidráhulico
    // ESTA FUNCION TIENE EN CUENTA LOS VALORES BAU ACTUALES Y VALORES TEORICOS DE LA EFICIENCIA .
    // ENTONCES PARA TENER EL VALOR DEL INCREMENTO DEBEMOS EMPEZAR EN EL BAU COMO ORIGEN
    name = validateNameIndicatorIep(name)
    let iep = 0 // (consumo /pib)/1000
    let anio = ""
    let k = 2
    let data_plot_iep = []
    var data_plot_return = []
    for (var i = 0; i < consumo.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        iep = consumo[i] / pib[i] / 1000
        //data_plot_dict = {"Año": anio, "Indicador intensidad energética primaria": iep};
        data_plot_dict.Año = anio
        data_plot_dict[name] = iep
        data_plot_iep.push(data_plot_dict)
    }
    data_plot_return["Indicador intensidad energética primaria"] = data_plot_iep
    createChartIndicador2(
        list_name,
        "Indicador intensidad energética primaria",
        name,
        data_plot_return,
        "chart_title_6",
        "line-chart-6",
        "graph-container-6"
    )
    return data_plot_return
}

function generationIndicatorsIEC(consumo, fe, pib, name) {
    // Generación con recurso hidráhulico
    // ESTA FUNCION TIENE EN CUENTA LOS VALORES BAU ACTUALES Y VALORES TEORICOS DE LA EFICIENCIA .
    // ENTONCES PARA TENER EL VALOR DEL INCREMENTO DEBEMOS EMPEZAR EN EL BAU COMO ORIGEN
    name = validateNameIndicatorIec(name)
    let iec = 0 // (consumo*fe) /pib
    let anio = ""
    let k = 2
    let data_plot_iec = []
    var data_plot_return = []

    for (var i = 0; i < consumo.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        iec = (consumo[i] * fe) / pib[i]
        data_plot_dict.Año = anio
        data_plot_dict[name] = iec
        data_plot_iec.push(data_plot_dict)
    }
    data_plot_return["Indicador intensidad de emisiones de carbono"] = data_plot_iec
    createChartIndicador3(
        list_name,
        "Indicador intensidad de emisiones de carbono",
        name,
        data_plot_return,
        "chart_title_7",
        "line-chart-7",
        "graph-container-7"
    )
    return data_plot_return
}

function generateDataIndicatorWithBau(sub_strategies_expansion, sub_strategies_upgrade, n) {
    let sub_strategies_key = Object.keys(sub_strategies_expansion)
    let data_model_expansion = []
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_expansion_name = sub_strategies_expansion[item].name
        let sub_strategies_expansion_value = parseFloat(sub_strategies_expansion[item].selected_value)
        let sub_strategies_expansion_fp = parseFloat(sub_strategies_expansion[item].fp)
        let sub_strategies_expansion_gen_historico = parseFloat(sub_strategies_expansion[item].generacion_historica)

        let data_model_expansion1 = modelExpansionEstrategy(
            n,
            sub_strategies_expansion_value,
            sub_strategies_expansion_fp,
            sub_strategies_expansion_name,
            sub_strategies_expansion_gen_historico
        )
        data_model_expansion.push(data_model_expansion1)
        //createChartExpansion(list_name, strategies_name, sub_strategies_name, data_model_expansion, "chart_title_3", "line-chart-3","graph-container-3");
    })

    let data_model_upgrade = []
    let sub_strategies_upgrade_key = Object.keys(sub_strategies_upgrade)

    sub_strategies_upgrade_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies_upgrade[item].name
        let sub_strategies_value = parseFloat(sub_strategies_upgrade[item].value) / 100
        let sub_strategies_n_LB = sub_strategies_upgrade[item].n_LB
        let sub_strategies_data = sub_strategies_upgrade[item].values_BAU
        let data_model_upgrade1 = modelUpgradeStrategy(
            n,
            sub_strategies_value,
            sub_strategies_data,
            sub_strategies_n_LB,
            sub_strategies_name
        )
        //createChartUpgrade(list_name, strategies_name, sub_strategies_name, plot_upgrade, "chart_title_4", "line-chart-4","graph-container-4");
        data_model_upgrade.push(data_model_upgrade1)
    })

    return [data_model_expansion, data_model_upgrade]
}

function generateDataIndicatorWithBau2(sub_strategies_expansion, sub_strategies_upgrade, n) {
    let sub_strategies_key = Object.keys(sub_strategies_expansion)
    let data_model_expansion = []
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_expansion_name = sub_strategies_expansion[item].name
        let sub_strategies_expansion_value = parseFloat(sub_strategies_expansion[item].value)
        let sub_strategies_expansion_fp = parseFloat(sub_strategies_expansion[item].fp)
        let sub_strategies_expansion_gen_historico = parseFloat(sub_strategies_expansion[item].generacion_historica)

        let data_model_expansion1 = modelExpansionEstrategy(
            n,
            sub_strategies_expansion_value,
            sub_strategies_expansion_fp,
            sub_strategies_expansion_name,
            sub_strategies_expansion_gen_historico
        )
        data_model_expansion.push(data_model_expansion1)
        //createChartExpansion(list_name, strategies_name, sub_strategies_name, data_model_expansion, "chart_title_3", "line-chart-3","graph-container-3");
    })

    let data_model_upgrade = []
    let sub_strategies_upgrade_key = Object.keys(sub_strategies_upgrade)

    sub_strategies_upgrade_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies_upgrade[item].name
        let sub_strategies_value = parseFloat(sub_strategies_upgrade[item].selected_value) / 100
        let sub_strategies_n_LB = sub_strategies_upgrade[item].n_LB
        let sub_strategies_data = sub_strategies_upgrade[item].values_BAU
        let data_model_upgrade1 = modelUpgradeStrategy(
            n,
            sub_strategies_value,
            sub_strategies_data,
            sub_strategies_n_LB,
            sub_strategies_name
        )
        //createChartUpgrade(list_name, strategies_name, sub_strategies_name, plot_upgrade, "chart_title_4", "line-chart-4","graph-container-4");
        data_model_upgrade.push(data_model_upgrade1)
    })

    return [data_model_expansion, data_model_upgrade]
}

function generateDataIndicatorWithValues(sub_strategies_expansion, sub_strategies_upgrade, n) {
    let sub_strategies_key = Object.keys(sub_strategies_expansion)
    let data_model_expansion = []
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_expansion_name = sub_strategies_expansion[item].name
        let sub_strategies_expansion_value = parseFloat(sub_strategies_expansion[item].selected_value)
        let sub_strategies_expansion_fp = parseFloat(sub_strategies_expansion[item].fp)
        let sub_strategies_expansion_gen_historico = parseFloat(sub_strategies_expansion[item].generacion_historica)

        let data_model_expansion1 = modelExpansionEstrategy(
            n,
            sub_strategies_expansion_value,
            sub_strategies_expansion_fp,
            sub_strategies_expansion_name,
            sub_strategies_expansion_gen_historico
        )
        data_model_expansion.push(data_model_expansion1)
        //createChartExpansion(list_name, strategies_name, sub_strategies_name, data_model_expansion, "chart_title_3", "line-chart-3","graph-container-3");
    })
    let data_model_upgrade = []
    let sub_strategies_upgrade_key = Object.keys(sub_strategies_upgrade)

    sub_strategies_upgrade_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies_upgrade[item].name
        let sub_strategies_value = parseFloat(sub_strategies_upgrade[item].selected_value) / 100
        let sub_strategies_n_LB = sub_strategies_upgrade[item].n_LB
        let sub_strategies_data = sub_strategies_upgrade[item].values_BAU
        let data_model_upgrade1 = modelUpgradeStrategy(
            n,
            sub_strategies_value,
            sub_strategies_data,
            sub_strategies_n_LB,
            sub_strategies_name
        )
        //createChartUpgrade(list_name, strategies_name, sub_strategies_name, plot_upgrade, "chart_title_4", "line-chart-4","graph-container-4");
        data_model_upgrade.push(data_model_upgrade1)
    })

    return [data_model_expansion, data_model_upgrade]
}

function createStrategyExpansionComplementary(sub_strategies, strategies_array_copia, n) {
    let sub_strategies_expansion = sub_strategies
    let ids_relatioated = sub_strategies_expansion.map((sub) => {
        let id_relationated = sub.id_relation
        return id_relationated
    })

    let strategies_copia = JSON.parse(JSON.stringify(strategies_array_copia))

    let strategies_array_copia_process = filterStrategiesByProcess(strategies_copia)
    let strategies_by_id_relationated = filterStrategiesByIdRelationated(
        strategies_array_copia_process,
        ids_relatioated
    )
    let sub_strategies_upgrade = strategies_by_id_relationated.models[1]
    let strategies_complementaries = sub_strategies_upgrade.strategies
        .filter((strategy) =>
            sub_strategies_expansion.some((strategy2) =>
                strategy2.id_relation.includes(strategy.id_relation)
            )
        )
        .map((sub_strategies_upgrade_list) => {
            let newSubStrategies = Object.assign({}, sub_strategies_upgrade_list)
            return newSubStrategies
        })
    let create_data_indicator = generateDataIndicatorWithBau(
        sub_strategies_expansion,
        strategies_complementaries,
        n
    )
    let create_data_indicator_generation = create_data_indicator[0]
    let create_data_indicator_consume = create_data_indicator[1]
    createGraphIndicator(create_data_indicator_generation, create_data_indicator_consume)
}

function createStrategyUpgradeComplementary(sub_strategies, strategies_array_copia, n) {
    let sub_strategies_upgrade = sub_strategies
    let ids_relatioated = sub_strategies_upgrade.map((sub) => {
        let id_relationated = sub.id_relation
        return id_relationated
    })
    let strategies_copia = JSON.parse(JSON.stringify(strategies_array_copia))
    let strategies_array_copia_process = filterStrategiesByProcess(strategies_copia)
    let strategies_by_id_relationated = filterStrategiesByIdRelationated(
        strategies_array_copia_process,
        ids_relatioated
    )
    let sub_strategies_expansion = strategies_by_id_relationated.models[0]
    let strategies_complementaries = sub_strategies_expansion.strategies
        .filter((strategy) =>
            sub_strategies_upgrade.some((strategy2) =>
                strategy2.id_relation.includes(strategy.id_relation)
            )
        )
        .map((sub_strategies_upgrade_list) => {
            let newSubStrategies = Object.assign({}, sub_strategies_upgrade_list)
            return newSubStrategies
        })
    let create_data_indicator = generateDataIndicatorWithBau2(
        strategies_complementaries,
        sub_strategies_upgrade,
        n
    )
    let create_data_indicator_generation = create_data_indicator[0]
    let create_data_indicator_consume = create_data_indicator[1]
    createGraphIndicator(create_data_indicator_generation, create_data_indicator_consume)
}

function emissionFactor(name) {
    let fe = 0
    if (name == "Generación eléctrica a partir de plantas térmicas") {
        fe = 0.126379
    } else if (name == "Generación eléctrica a partir de plantas de Auto y Cogeneración") {
        fe = 0.126379
    } else {
        fe = 0
    }
    return fe
}

function modifyName(name) {
    let str = name
    // let keyword = "de";
    // let words = str.split(" ");
    // let index = words.indexOf(keyword);
    // let result = words.slice(index).join(" ");
    let keyword = "de"
    let index = str.indexOf(keyword)
    let result = str.slice(index + keyword.length).trim()
    return result
}

function prepareDataTopsis(eficiency, iep, iec, name) {
    console.log("---prepareDataTopsis---")
    console.log("eficiency",eficiency)
    let parent_object = {}
    let name_plant = modifyName(name)
    let efi = Object.values(eficiency)[0].slice(-1)[0]
    let efi_last_value = Object.values(efi)[1]
    let efi_last_name = Object.keys(efi)[1]

    console.log("efi",efi)
    console.log("efi_last_value",efi_last_value)
    console.log("efi_last_name",efi_last_name)

    let iep_last = Object.values(iep)[0].slice(-1)[0]
    let iep_las_value = Object.values(iep_last)[1]
    let iep_las_name = Object.keys(iep_last)[1]

    let iec_last = Object.values(iec)[0].slice(-1)[0]
    let iec_last_value = Object.values(iec_last)[1]
    let iec_last_name = Object.keys(iec_last)[1]

    let data_topsis_return = Object.assign({}, parent_object, {
        [name_plant]: [
            {
                [efi_last_name]: efi_last_value,
                [iep_las_name]: iep_las_value,
                [iec_last_name]: iec_last_value,
            },
        ],
    })
    console.log("data_topsis_return",data_topsis_return)
    return data_topsis_return
}

function createDataChartTopsis(data) {
    let dataTopsis = JSON.parse(data)
    let keys = Object.keys(dataTopsis)
    keys.forEach(function (item) {
        let alternatives = dataTopsis[item]["alternatives"]
        let data_graph = []
        let array_alternatives = []
        let dict_graph = {}
        dict_graph.Año = " "
        dict_graph[alternatives] = dataTopsis[item]["performance score"]
        array_alternatives.push(dict_graph)
        data_graph["Clasificación de estrategias"] = array_alternatives
        createChartTopsis(
            list_name,
            "Clasificación de estrategias",
            alternatives,
            data_graph,
            "chart_title_8",
            "line-chart-8",
            "graph-container-8"
        )
    })
}

function createTotalValueForSave(generacion,consumo){
    let total_data_generation = []
    let total_data_consumption = []
    let data_consumption_emissions = []
    let n_year = validateDate();
    let n = n_year[0]
    const fe_const = 0.126379
    let pib = [
        344.1612833, 355.4685381, 367.8705797, 380.837696, 394.8857455, 408.9742253, 423.1216551,
        437.1906672, 451.7446956,
    ]

    let keys_genrartion = Object.keys(generacion)
    keys_genrartion.forEach(function (item, index) {
        let genration_item = generacion[item]
        let consume_item = consumo[item]
        let data_generacion_total = modifyData(genration_item)
        let data_consumo_total = modifyData(consume_item)
        let data_generacion = data_generacion_total[0]
        let name = data_generacion_total[1]
        let data_consumo = data_consumo_total[0]
        // saco el ultimo valor y lo almaceno en un acumulador
        const [lastElementGen] = [...data_generacion].reverse();
        total_data_generation.push(lastElementGen)
        const [lastElementCom] = [...data_consumo].reverse();
        total_data_consumption.push(lastElementCom)
        let fe = emissionFactor(name)
        if (fe !== 0){
            const [lastElementComEm] = [...data_consumo].reverse();
            data_consumption_emissions.push(lastElementComEm)
        }
    })
    const sumGen = total_data_generation.reduce((accumulator, currentValue) => accumulator + currentValue);
    const sumCon = total_data_consumption.reduce((accumulator, currentValue) => accumulator + currentValue);
    const sumConEmissions = data_consumption_emissions.length > 0 ? data_consumption_emissions.reduce((accumulator, currentValue) => accumulator + currentValue) : 0;
    let eficiency = sumGen / sumCon
    let iep = (sumCon / pib[n-1] ) /1000
    let iec = (sumConEmissions*fe_const )/pib[n-1]
    for_save_indicators.push(eficiency,iep,iec)
}

function createGraphIndicator(create_data_indicator_generation, create_data_indicator_consume) {
    let generacion = create_data_indicator_generation
    let consumo = create_data_indicator_consume
    //datos de pib desde 2022 hasta 2030, no es necesario agregar año porque el sistem recorre hasta el año que necesita
    let pib = [
        344.1612833, 355.4685381, 367.8705797, 380.837696, 394.8857455, 408.9742253, 423.1216551,
        437.1906672, 451.7446956,
    ]
    //funcion solo para el guardado de varibles totales
    //para posterior comparacion con otros escenarios
    for_save_generation.push(...generacion)
    for_save_consumption.push(...consumo)

    let keys_genrartion = Object.keys(generacion)
    keys_genrartion.forEach(function (item, index) {
        let genration_item = generacion[item]
        let consume_item = consumo[item]

        let data_generacion_total = modifyData(genration_item)
        let data_consumo_total = modifyData(consume_item)

        let data_generacion = data_generacion_total[0]
        let name = data_generacion_total[1]
        let data_consumo = data_consumo_total[0]
        let fe = emissionFactor(name)
        let eficiency = generationIndicatorEficiency(data_generacion, data_consumo, name)
        let iep = generationIndicatorsIEP(data_consumo, pib, name)
        let iec = generationIndicatorsIEC(data_consumo, fe, pib, name)
        let values = prepareDataTopsis(eficiency, iep, iec, name)




        data_topsis.push(values)
    })
    console.log("data_topsis GEN", data_topsis)
}

function plotDataStrategies(strategies) {
    let strategiesModels = strategies.models
    let n_and_year = validateDate()
    let n = n_and_year[0]

    let strategiesName = getStrategieName()

    if (
        Object.entries(strategiesModels.filter((model) => strategiesName[0].includes(model.name)))
            .length != 0 &&
        Object.entries(strategiesModels.filter((model) => strategiesName[1].includes(model.name)))
            .length != 0
    ) {
        let a = strategiesModels[0]
        let b = strategiesModels[1]

        if (
            Object.entries(
                b.strategies.filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
            ).length != 0
        ) {
            //aqui grafica cuando tiene las dos estrategias y que estan relacionadas entre si
            let strategies_relationated = b.strategies
                .filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
                .map((sub_strategies) => {
                    let newSubStrategies = Object.assign({}, sub_strategies, {
                        values_BAU: a.strategies
                            .filter((strategyValue) =>
                                strategyValue.id_relation.includes(sub_strategies.id_relation)
                            )
                            .map((sub_strategies_values) => {
                                let newSubStrategies = modelExpansionEstrategyOnlyData(
                                    n,
                                    parseFloat(sub_strategies_values.selected_value),
                                    sub_strategies_values.fp,
                                    sub_strategies_values.generacion_historica
                                )
                                return newSubStrategies
                            })[0],
                    })
                    return newSubStrategies
                })
            let sub_str_not_included = b.strategies
                .filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
                .map((sub) => {
                    let new_ids = sub.id_relation
                    return new_ids
                })
            generateGhapExpansion(a.strategies, n, strategiesName[0])
            generateGhapUpgrade(strategies_relationated, n, strategiesName[1])

            if (
                Object.entries(
                    b.strategies.filter((strategy) => !sub_str_not_included.includes(strategy.id_relation))
                ).length != 0
            ) {
                let sub_str_not_relationed = b.strategies.filter(
                    (strategy) => !sub_str_not_included.includes(strategy.id_relation)
                )
                generateGhapUpgrade(sub_str_not_relationed, n, strategiesName[1])
            }
        } else if (
            Object.entries(
                b.strategies.filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation !== strategy.id_relation)
                )
            ).length != 0
        ) {
            //aqui grafica cuando tiene las dos estrategias pero esta no esta relacionada con las sub estrategias de expansion
            let sub_strategies_no_relationed = b.strategies.filter((strategy) =>
                a.strategies.some((strategy2) => strategy2.id_relation !== strategy.id_relation)
            )
            generateGhapExpansion(a.strategies, n, strategiesName[0])
            generateGhapUpgrade(sub_strategies_no_relationed, n, strategiesName[1])
        } else {
            //aqui grafica cuando tiene las dos estrategias pero ninguna esta relacionada entre si //nunca entra pero por si acaso
            generateGhapExpansion(a.strategies, n, strategiesName[0])
            generateGhapUpgrade(b.strategies, n, strategiesName[1])
        }
    } else {
        let strategiesModelsKeys = Object.keys(strategiesModels)
        strategiesModelsKeys.forEach(function (items, index) {
            let strategies_name = strategiesModels[items].name
            let sub_strategies = strategiesModels[items].strategies

            if (strategies_name == "Estrategias de expansión") {
                generateGhapExpansion(sub_strategies, n, strategies_name)
            } else if (strategies_name == "Estrategias de actualización") {
                generateGhapUpgrade(sub_strategies, n, strategies_name)
            }
        })
    }
}

function plotDataIndicators(strategies) {
    let strategiesModels = strategies.models
    let n_and_year = validateDate()
    let n = n_and_year[0]
    let strategies_array_copia = const_strategies

    let strategiesName = getStrategieName()
    if (
        Object.entries(strategiesModels.filter((model) => strategiesName[0].includes(model.name)))
            .length != 0 &&
        Object.entries(strategiesModels.filter((model) => strategiesName[1].includes(model.name)))
            .length != 0
    ) {
        let a = strategiesModels[0]
        let b = strategiesModels[1]
        if (
            Object.entries(
                b.strategies.filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
            ).length != 0
        ) {
            //aqui grafica cuando tiene las dos estrategias y que estan relacionadas entre si
            let strategies_relationated = b.strategies
                .filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
                .map((sub_strategies) => {
                    let newSubStrategies = Object.assign({}, sub_strategies, {
                        values_BAU: a.strategies
                            .filter((strategyValue) =>
                                strategyValue.id_relation.includes(sub_strategies.id_relation)
                            )
                            .map((sub_strategies_values) => {
                                let newSubStrategies = modelExpansionEstrategyOnlyData(
                                    n,
                                    parseFloat(sub_strategies_values.selected_value),
                                    sub_strategies_values.fp,
                                    sub_strategies_values.generacion_historica
                                )
                                return newSubStrategies
                            })[0],
                    })
                    return newSubStrategies
                })

            let strategies_relationated_expansion = a.strategies.filter((strategy) =>
                b.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
            )
            let sub_str_not_included = b.strategies
                .filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
                .map((sub) => {
                    let new_ids = sub.id_relation
                    return new_ids
                })

            let sub_str_not_included_expansion = a.strategies
                .filter((strategy) =>
                    b.strategies.some((strategy2) => strategy2.id_relation.includes(strategy.id_relation))
                )
                .map((sub) => {
                    let new_ids = sub.id_relation
                    return new_ids
                })
            let create_data_indicator = generateDataIndicatorWithValues(
                strategies_relationated_expansion,
                strategies_relationated,
                n
            )
            let create_data_indicator_generation = create_data_indicator[0]
            let create_data_indicator_consume = create_data_indicator[1]
            createGraphIndicator(create_data_indicator_generation, create_data_indicator_consume)

            if (
                Object.entries(
                    b.strategies.filter((strategy) => !sub_str_not_included.includes(strategy.id_relation))
                ).length != 0
            ) {
                let sub_str_not_relationed = b.strategies.filter(
                    (strategy) => !sub_str_not_included.includes(strategy.id_relation)
                )
                createStrategyUpgradeComplementary(sub_str_not_relationed, strategies_array_copia, n)
            }
            if (
                Object.entries(
                    a.strategies.filter(
                        (strategy) => !sub_str_not_included_expansion.includes(strategy.id_relation)
                    )
                ).length != 0
            ) {
                let sub_str_not_relationed = a.strategies.filter(
                    (strategy) => !sub_str_not_included_expansion.includes(strategy.id_relation)
                )
                createStrategyExpansionComplementary(sub_str_not_relationed, strategies_array_copia, n)
            }
        } else if (
            Object.entries(
                b.strategies.filter((strategy) =>
                    a.strategies.some((strategy2) => strategy2.id_relation !== strategy.id_relation)
                )
            ).length != 0
        ) {
            // aquí gráfica cuando tiene las dos estrategias pero esta no esta relacionada con las sub estrategias de expansion
            let sub_strategies_no_relationed = b.strategies.filter((strategy) =>
                a.strategies.some((strategy2) => strategy2.id_relation !== strategy.id_relation)
            )
            /** Se puede usar las mismas funciones de cuanto no fueron seleccionadas las dos estrategias (expansioon y actualizacion)
             * No es necesario verificar el tipo de estrategia ya que el filtro anterior siempre devuelve
             * las sub estrategias de actualizacion
             */
            createStrategyExpansionComplementary(a.strategies, strategies_array_copia, n)
            createStrategyUpgradeComplementary(sub_strategies_no_relationed, strategies_array_copia, n)
        } else {
            //aqui grafica cuando tiene las dos estrategias pero ninguna esta relacionada entre si //nunca entra pero por si acaso
            //generateGhapExpansion(a.strategies,n,strategiesName[0]);
            //generateGhapUpgrade(b.strategies,n,strategiesName[1])
        }
    } else {
        let strategiesModelsKeys = Object.keys(strategiesModels)
        strategiesModelsKeys.forEach(function (items, index) {
            let strategies_name = strategiesModels[items].name
            let sub_strategies = strategiesModels[items].strategies
            if (strategies_name == "Estrategias de expansión") {
                createStrategyExpansionComplementary(sub_strategies, strategies_array_copia, n)
            } else if (strategies_name == "Estrategias de actualización") {
                createStrategyUpgradeComplementary(sub_strategies, strategies_array_copia, n)
            }
        })
    }
    createTotalValueForSave(for_save_generation, for_save_consumption)
}

function modelExpansionEstrategyOnlyData(n, valorObjetivo, fp, generacion_historica) {
    let c_i_base = generacion_historica / (8760* fp)
    var increment = (valorObjetivo - c_i_base)/ n
    var data = []
    var data_Return = []
    let gp = 0

    let creaIncrement = c_i_base + increment
    for (let a = 0; a < n; a++) {
        data.push(creaIncrement)
        creaIncrement = creaIncrement + increment
    }
    for (let i = 0; i < data.length; i++) {
        gp = data[i] * fp * 8760
        data_Return.push(gp)
    }
    return data_Return
}

function modelExpansionEstrategy(n, valorObjetivo, fp, name, generacion_historica) {
    let c_i_base = generacion_historica / (8760* fp)
    var increment = (valorObjetivo - c_i_base)/ n
    var data = []
    var data_plot = []
    var data_plot_return = []
    let j = 2
    let gp = 0

    let creaIncrement = c_i_base + increment
    for (let a = 0; a < n; a++) {
        data.push(creaIncrement)
        creaIncrement = creaIncrement + increment
    }
    for (let i = 0; i < data.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++
        gp = data[i] * fp * 8760
        data_plot_dict.Año = anio
        data_plot_dict[name] = gp
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Estrategias de expansión"] = data_plot
    return data_plot_return
}

function modelUpgradeStrategy(n, nj, dataIn, n_LB, name) {
    // Generación con recurso hidráhulico
    // ESTA FUNCION TIENE EN CUENTA LOS VALORES BAU ACTUALES Y VALORES TEORICOS DE LA EFICIENCIA .
    // ENTONCES PARA TENER EL VALOR DEL INCREMENTO DEBEMOS EMPEZAR EN EL BAU COMO ORIGEN
    let cp = 0
    let j = 2
    var data = []
    var data_plot = []
    var data_plot_return = []
    var incrementNj = (nj - n_LB) / n //llamar al valor minimo n_LB
    let creaIncrement = n_LB + incrementNj
    for (let a = 0; a < n; a++) {
        data.push(creaIncrement)
        creaIncrement = creaIncrement + incrementNj
    }

    for (let i = 0; i < data.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++

        cp = dataIn[i] / data[i]
        data_plot_dict.Año = anio
        data_plot_dict[name] = cp
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Estrategias de actualización"] = data_plot
    return data_plot_return
}

/* Desde aca se puede seguir ajustando */

//var strategies_const
function calculateElectricConsumptionVehicles(n, rm, vkt, name) {
    var increment = rm / n
    var data = []
    var data_plot = []
    var data_plot_return = []
    let j = 2
    let ce_vehicles = 0

    let creaIncrement = increment
    for (let a = 0; a < n; a++) {
        data.push(creaIncrement)
        creaIncrement = creaIncrement + increment
    }
    for (let i = 0; i < data.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++
        ce_vehicles = (0.000001) * data[i] * vkt[i]
        data_plot_dict.Año = anio
        data_plot_dict[name] = ce_vehicles
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Estrategias de electrificación en el transporte"] = data_plot
    return [data_plot_return, data_plot]
}

function calculateElectricConsumptionVehiclesRmConstant(n, rm, vkt, name) {
    // var increment = rm / n
    // var data = []
    var data_plot = []
    var data_plot_return = []
    let j = 2
    let pci = 45329.5
    let den_rel = 0.7405
    let ce_vehicles = 0

    // let creaIncrement = increment
    // for (let a = 0; a < n; a++) {
    // 	data.push(creaIncrement)
    // 	creaIncrement = creaIncrement + increment
    // }
    for (let i = 0; i < vkt.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++
        ce_vehicles = (0.000000001 * vkt[i] * pci * den_rel) / rm / 3.6
        data_plot_dict.Año = anio
        data_plot_dict[name] = ce_vehicles
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Estrategias de electrificación en el transporte"] = data_plot
    return [data_plot_return, data_plot]
}

function calculateVkt(n, avkt, nv, porcentaje_incremento) {
    // el calculo del numero de vehiculos utiliza la formula  x1 = x2 / (% + 1) donde:
    // x1 valor a calular en año anteior al seleccionado
    // x2 valor del año actual
    // % porcentaje del año actual
    porcentaje_incremento = porcentaje_incremento.slice(0, n)
    let porcen_rever = porcentaje_incremento.reverse()
    var data = []
    var array_vkt = []
    let vkt = 0

    let creaIncrement = nv
    for (let a = 0; a < n; a++) {
        data.push(creaIncrement)
        creaIncrement = creaIncrement / (porcen_rever[a] + 1)
    }
    data.reverse()
    for (let i = 0; i < data.length; i++) {
        vkt = avkt * data[i]
        array_vkt.push(vkt)
    }
    return array_vkt
}

function generateGhapTransportElectrification(sub_strategies, n, strategies_name) {
    //console.log("---generateGhapTransportElectrification---  ")
    let sub_strategies_key = Object.keys(sub_strategies)
    sub_strategies_key.forEach(function (item, index) {
        let sub_strategies_name = sub_strategies[item].name
        let sub_strategies_value = parseFloat(sub_strategies[item].selected_value) // NV numero de vehiculos
        let sub_strategies_value_aux_mod = sub_strategies[item].selected_value_aux // Rendimiento del motor
        let sub_strategies_avkt = parseFloat(sub_strategies[item].avkt)
        let sub_strategies_incremto_n_vehiculos = sub_strategies[item].incremto_n_vehiculos
        let sub_strategies_value_aux
        let data_ce_vehicles

        if (typeof sub_strategies_value_aux_mod === "string") {
            sub_strategies_value_aux = parseFloat(sub_strategies[item].selected_value_aux) //rendimiento del motor desde slider
            let vkt = calculateVkt(n, sub_strategies_avkt, sub_strategies_value, sub_strategies_incremto_n_vehiculos)
            //utiliza de entrada el promedio de km recorridos(avkt), # de vehículos eléctricos (nv)
            let data_consump_vehic = calculateElectricConsumptionVehicles(
                n,
                sub_strategies_value_aux,
                vkt,
                sub_strategies_name
            )
            data_ce_vehicles = data_consump_vehic[0]
        } else if (typeof sub_strategies_value_aux_mod === "boolean") {
            sub_strategies_value_aux = parseFloat(sub_strategies[item].rm_Km_Lge) // Rendimiento del motor constante
            let vkt = calculateVkt(n, sub_strategies_avkt, sub_strategies_value, sub_strategies_incremto_n_vehiculos)
            //utiliza de entrada el promedio de km recorridos(avkt), # de vehículos eléctricos (nv)
            let data_consump_vehic = calculateElectricConsumptionVehiclesRmConstant(
                n,
                sub_strategies_value_aux,
                vkt,
                sub_strategies_name
            )
            data_ce_vehicles = data_consump_vehic[0]
        }
        createChartExpansion(
            list_name,
            strategies_name,
            sub_strategies_name,
            data_ce_vehicles,
            "chart_title_3",
            "line-chart-3",
            "graph-container-3"
        )
    })
}

function calculateElectricConsumptionEndUse(n, pi, np, nb, ce_bau, name, np_constant) {
	var incrementPi = pi / n
    var dataNp = []
    var dataPi = []
    var data_plot = []
    var data_plot_return = []
    let j = 2
    let ce = 0
	if(!np_constant){
		var incrementNp = np / n
		let creaIncrementNp = incrementNp
		for (let a = 0; a < n; a++) {
			dataNp.push(creaIncrementNp)
			creaIncrementNp = creaIncrementNp + incrementNp
		}
	}
    let creaIncrementPi = incrementPi
    for (let a = 0; a < n; a++) {
        dataPi.push(creaIncrementPi)
        creaIncrementPi = creaIncrementPi + incrementPi
    }
    for (let i = 0; i < dataPi.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++
		if(!np_constant){
			ce = ce_bau[i] * (1 - (1 - nb / dataNp[i]) * dataPi[i])
		}else{
        	ce = ce_bau[i] * (1 - (1 - nb / np) * dataPi[i])
		}
        data_plot_dict.Año = anio
        data_plot_dict[name] = ce
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Estrategias de actualización tecnológica"] = data_plot
    return [data_plot_return, data_plot]
}

function generateGhapTechnologicalUpdate(sub_strategies, n, strategies_name) {
    //console.log("-----generateGhapTechnologicalUpdate ---  ")
    let sub_strategies_key = Object.keys(sub_strategies)
    sub_strategies_key.forEach(function (item, index) {
        //utiliza de entrada eficiencia base nb , consumo electico bau ce_bau
        let sub_strategies_name = sub_strategies[item].name
        let sub_strategies_value = parseFloat(sub_strategies[item].selected_value) / 100 // porcentaje de incorporacion
        let sub_strategies_value_aux_mod = sub_strategies[item].selected_value_aux // np eficiencia deseada
        let sub_strategies_value_aux
		let np_constant = false                                                    //variable que indica si eficiencia deseada ha sido modificada o no
        if (typeof sub_strategies_value_aux_mod === "string") {
            sub_strategies_value_aux = parseFloat(sub_strategies[item].selected_value_aux) / 100 // np eficiencia deseada
        } else if (typeof sub_strategies_value_aux_mod === "boolean") {
            sub_strategies_value_aux = sub_strategies[item].np / 100                    // np eficiencia deseada
			np_constant = true
        }
        let sub_strategies_nb = parseFloat(sub_strategies[item].nb)
        let sub_strategies_ce_bau = sub_strategies[item].ce_bau.map(
            (ce_bau) => ce_bau * sub_strategies[item].consumption_percent
        )
        //utiliza de entrada eficiencia base nb , consumo electico bau ce_bau
        let data_ce_consumpt = calculateElectricConsumptionEndUse(
            n,
            sub_strategies_value,
            sub_strategies_value_aux,
            sub_strategies_nb,
            sub_strategies_ce_bau,
            sub_strategies_name,
			np_constant
        )
        let data_ce = data_ce_consumpt[0]
        createChartUpgrade(
            list_name,
            strategies_name,
            sub_strategies_name,
            data_ce,
            "chart_title_4",
            "line-chart-4",
            "graph-container-4"
        )
    })
}

function dataGraphStrategiesEndUse(strategies) {
    //console.log(" --- dataGraphStrategiesEndUse --- ")
    let strategiesModels = strategies.models
    let n_and_year = validateDate()
    let n = n_and_year[0]
    //let strategiesName = getStrategieName()
    let strategiesModelsKeys = Object.keys(strategiesModels)
    strategiesModelsKeys.forEach(function (items, index) {
        let strategies_name = strategiesModels[items].name
        let sub_strategies = strategiesModels[items].strategies
        if (strategies_name == "Estrategias de electrificación en el transporte") {
            generateGhapTransportElectrification(sub_strategies, n, strategies_name)
        } else if (strategies_name == "Estrategias de actualización tecnológica") {
            generateGhapTechnologicalUpdate(sub_strategies, n, strategies_name)
        }
    })
}

function sumStrategyDatawithAccumulation(data_model_electrification) {
    let arrays = data_model_electrification.map((arr) => arr.map((obj) => Object.values(obj)[1]))
    let sumaTotal = 38.88612 // se inicia en este valor ya que para el analisis desde 2022 -2030 para el año 2021 ya se tiene este valor de electrificación
    const resultado = []
    for (let i = 0; i < arrays[0].length; i++) {
        let suma = 0
        for (let j = 0; j < arrays.length; j++) {
            suma += arrays[j][i]
        }
        sumaTotal += suma
        resultado.push(sumaTotal)
    }
    return resultado
}

function sumStrategyData(data_model_electrification) {
    //console.log("---sumStrategyData-----")
    let result = data_model_electrification.reduce((acc, curr) => {
        let array_sum = acc.map((v, i) => {
            let sum
            if (Number.isInteger(v) || typeof v === "number") {
                sum = v + Object.values(curr[i])[1]
            } else {
                sum = Object.values(v)[1] + Object.values(curr[i])[1]
            }
            return sum
        })
        return array_sum
    })
    return result
}

function totalSumStrategyData(consumption_electrical_vehicle, consumption_technological_upgrade) {
    //console.log(" -----totalSumStrategyData--- ")
    let result
    if (consumption_electrical_vehicle.length !== consumption_technological_upgrade.length) {
        console.log("Hubo un error en el sistema por favor verifique el tamaño de los arrays ")
    } else {
        result = consumption_electrical_vehicle.map(
            (num, index) => num + consumption_technological_upgrade[index]
        )
    }
    return result
}

function generatePerCapitaConsumptionindicator(total_elect_consump, poblacion) {
    let c_per_cap = 0
    let data_plot_c_per_cap = []
    let k = 2
    let anio_c_per_cap = ""
    let data_plot_return = []
    for (var i = 0; i < total_elect_consump.length; i++) {
        let data_plot_dict = {}
        anio_c_per_cap = "202" + k
        if (k > 9) {
            k = 0
            anio_c_per_cap = "203" + k
        }
        k++
        c_per_cap = (total_elect_consump[i] / poblacion[i]) * 1000
        data_plot_dict.Año = anio_c_per_cap
        data_plot_dict["Consumo per cápita"] = c_per_cap
        data_plot_c_per_cap.push(data_plot_dict)
    }
    data_plot_return["Indicador consumo per cápita"] = data_plot_c_per_cap
    createChartIndicador1(
        list_name,
        "Indicador consumo per cápita",
        "Consumo per cápita",
        data_plot_return,
        "chart_title_5",
        "line-chart-5",
        "graph-container-5"
    )
    return data_plot_return
}

function generateEnergyintensityindicator(total_elect_consump, pib_billones_usd) {
    let energy_intensity = 0
    let data_plot_energy_intensity = []
    let k = 2
    let anio_energy_intensity = ""
    let data_plot_return = []
    for (var i = 0; i < total_elect_consump.length; i++) {
        let data_plot_dict = {}
        anio_energy_intensity = "202" + k
        if (k > 9) {
            k = 0
            anio_energy_intensity = "203" + k
        }
        k++
        energy_intensity = total_elect_consump[i] / pib_billones_usd[i] / 1000
        data_plot_dict.Año = anio_energy_intensity
        data_plot_dict["Intensidad energética"] = energy_intensity
        data_plot_energy_intensity.push(data_plot_dict)
    }
    data_plot_return["Indicador intensidad energética"] = data_plot_energy_intensity
    createChartIndicador2(
        list_name,
        "Indicador intensidad energética",
        "Intensidad energética",
        data_plot_return,
        "chart_title_6",
        "line-chart-6",
        "graph-container-6"
    )
    return data_plot_return
}

function generateAvoidEmissionsIndicator(total_elect_consump, ce_bau, fe) {
    let avoid_emissions = 0
    let data_plot_avoid_emissions = []
    let k = 2
    let anio_avoid_emissions = ""
    let data_plot_return = []
    for (var i = 0; i < total_elect_consump.length; i++) {
        let data_plot_dict = {}
        anio_avoid_emissions = "202" + k
        if (k > 9) {
            k = 0
            anio_avoid_emissions = "203" + k
        }
        k++
        avoid_emissions = (ce_bau[i] - total_elect_consump[i]) * fe
        data_plot_dict.Año = anio_avoid_emissions
        data_plot_dict["Emisiones evitadas"] = avoid_emissions
        data_plot_avoid_emissions.push(data_plot_dict)
    }
    data_plot_return["Indicador emisiones evitadas"] = data_plot_avoid_emissions
    createChartIndicador3(
        list_name,
        "Indicador emisiones evitadas",
        "Emisiones evitadas",
        data_plot_return,
        "chart_title_7",
        "line-chart-7",
        "graph-container-7"
    )
    return data_plot_return
}

function createGraphIndicatorEndUse(total_elect_consump, ce_bau, poblacion, pib_billones_usd) {
    let fe = 0.2
    //total_elect_consump es quien determina hasta donde se recorren los arrays complementarios que contienen datos del 2022 hasta 2030
    let c_per_cap = generatePerCapitaConsumptionindicator(total_elect_consump, poblacion)
    let energy_intensity = generateEnergyintensityindicator(total_elect_consump, pib_billones_usd)
    let avoid_emissions = generateAvoidEmissionsIndicator(total_elect_consump, ce_bau, fe)
    //seleccion de ultimo valor del array (se hace para obtener los indicadores que se van guardar)
    let last_c_per_cap = Object.values(Object.values(c_per_cap)[0].at(-1))[1]
    let last_energy_intensity = Object.values(Object.values(energy_intensity)[0].at(-1))[1]
    let last_avoid_emissions = Object.values(Object.values(avoid_emissions)[0].at(-1))[1]
    //array order: enviromental_indicator, economic_indicator, energy_indicator
    for_save_indicators.push(last_avoid_emissions,last_energy_intensity,last_c_per_cap)
}

function createDataForTospsis(impact, population, pib_usd, ce_bau_projected, name) {
    let parent_object = {}
    let fe = 0.2
    let data_topsis_return = Object.assign({}, parent_object, {
        [name]: [
            {
                ["Consumo per capita"]: (impact / population) * 1000,
                ["Intensidad energética"]: impact / pib_usd / 1000,
                ["Emisiones evitadas"]: (ce_bau_projected - impact) * fe,
            },
        ],
    })
    return data_topsis_return
}

function generateDataIndicatorEndUse(
    sub_strategies_electrification,
    sub_strategies_technological,
    n
) {
    //console.log("-----generateDataIndicatorEndUse---------  ")
    let data_model_electrification = [] // alamacen los valores de todas las estrategias de electrificacion del transporte
    let lightweight_vehicles = []
    let lightweight_vehicles_array = [] //almacena los valores de las estrategegias de electr del transporte ligero
    let heavy_vehicles = []
    let heavy_vehicles_array = [] //almacena los valores de las estrategegias de electr del transporte pesado
    console.log("data_topsis END", data_topsis)
    data_topsis = []
    let sub_strategies_key = Object.keys(sub_strategies_electrification)
    sub_strategies_key.forEach(function (item, index) {
        //let data_electrification = []
        let sub_strategies_name = sub_strategies_electrification[item].name
        let sub_strategies_value_mod = sub_strategies_electrification[item].selected_value //NV numero de vehiculos
        let sub_strategies_value_aux_mod = sub_strategies_electrification[item].selected_value_aux //  Rendimiento del motor
        let sub_strategies_avkt = parseFloat(sub_strategies_electrification[item].avkt)
        let sub_strategies_incremto_n_vehiculos = sub_strategies_electrification[item].incremto_n_vehiculos
        let sub_strategies_value
        let sub_strategies_value_aux
        if (typeof sub_strategies_value_mod === "string") {
            sub_strategies_value = parseFloat(sub_strategies_electrification[item].selected_value) // numero de vehiculos desde sliders
        } else if (sub_strategies_value_mod === undefined) {
            let nv_default = sub_strategies_electrification[item].num_vehic_elect // numero de vehiculos desde db
            sub_strategies_value = parseFloat(nv_default[n - 1])
        }
        //si la variable selected_value_aux no existe en el objeto significa que el usuario no elegio esa estrategia
        // si la variable selected_value_aux existe pero es false significa que el usuario eleigio la estrategia pero no selecciono el RM
        // si la variable selected_value_aux  es strgin significa que el usuario eligio la estrategia y modifico El rendimiento del motor
        //utiliza de entrada el promedio de km recorridos(avkt), # de vehículos eléctricos (nv)
        let vkt = calculateVkt(n, sub_strategies_avkt, sub_strategies_value, sub_strategies_incremto_n_vehiculos)
        let data_ce_vehicles
        if (typeof sub_strategies_value_aux_mod === "string") {
            sub_strategies_value_aux = parseFloat(sub_strategies_electrification[item].selected_value_aux) //rendimiento del motor desde slider
            //Devuelve la multiplicacion de VKT * rendimiento del motor
            data_ce_vehicles = calculateElectricConsumptionVehicles(
                n,
                sub_strategies_value_aux,
                vkt,
                sub_strategies_name
            )
        } else if (typeof sub_strategies_value_aux_mod === "boolean" || sub_strategies_value_aux_mod === undefined) {
            sub_strategies_value_aux = parseFloat(sub_strategies_electrification[item].rm_Km_Lge) // Rendimiento del motor constante
            data_ce_vehicles = calculateElectricConsumptionVehiclesRmConstant(
                n,
                sub_strategies_value_aux,
                vkt,
                sub_strategies_name
            )
        }
        let data_ce_ve_without_name = data_ce_vehicles[1]
        data_model_electrification.push(data_ce_ve_without_name)
        if (sub_strategies_electrification[item].id_tipo_vehiculo == "ve001") {
            // data_electrification.push(data_ce_ve_without_name)
            // let last_value_cv = data_electrification[0][data_electrification[0].length - 1]
            //lightweight_vehicles.push(Object.values(last_value_cv)[1])
            lightweight_vehicles_array.push(data_ce_ve_without_name)
        } else {
            // data_electrification.push(data_ce_ve_without_name)
            // let last_value_cv = data_electrification[0][data_electrification[0].length - 1]
            //heavy_vehicles.push(Object.values(last_value_cv)[1])
            heavy_vehicles_array.push(data_ce_ve_without_name)
        }
    })

    lightweight_vehicles = sumStrategyData(lightweight_vehicles_array)  //suma todos lo valores de los arreglos para cada año
    heavy_vehicles = sumStrategyData(heavy_vehicles_array)

    //se inicializan valores para la suma ya que para los años antes del analisis ya habia vehiculos en colombia 
    let lightweight_sum = lightweight_vehicles.reduce((accumulator, currentValue) => {
        // suma todos los totales de todos los años para devolver un unico valor
        return accumulator + currentValue
    }, 22.400)
    let heavy_sum = heavy_vehicles.reduce((accumulator, currentValue) => {
        return accumulator + currentValue
    }, 16.48)

    let data_model_upgrade = []
    let ce_bau = [],
        poblacion = [],
        pib_billones_usd = []
    let consumption_percent_residential = 0.365870975887343
    let consumption_percent_c_p = 0.247125862010456
    let consumption_percent_industrial = 0.3870031621022
    let impact_total_residential_demand
    let impact_total_demand_commercial_public
    let impact_total_industrial_demand
	let np_constant_= false
    let sub_strategies_upgrade_key = Object.keys(sub_strategies_technological)
    sub_strategies_upgrade_key.forEach(function (item, index) {
        //utiliza de entrada rficirencia base nb , consumo electico bau ce_bau
        //console.log("----technologicalUpgrade  ---- ")
        let data_upgrade = []
        let sub_strategies_name = sub_strategies_technological[item].name
        let sub_strategies_value_mod = sub_strategies_technological[item].selected_value // pi porcentajde de incorporacion
        let sub_strategies_value_aux_mod = sub_strategies_technological[item].selected_value_aux // nd eficiencia deseada
        let sub_strategies_value
        let sub_strategies_value_aux
        if (typeof sub_strategies_value_mod === "string") {
            sub_strategies_value = parseFloat(sub_strategies_technological[item].selected_value) / 100 // pi porcentajde de incorporacion
        } else if (sub_strategies_value_mod === undefined) {
			let pi_default = sub_strategies_technological[item].pi_bau
            sub_strategies_value = parseFloat(pi_default[n-1]) // pi porcentaje de incorporacion desde db
        }
        if (typeof sub_strategies_value_aux_mod === "string") {
            sub_strategies_value_aux =
                parseFloat(sub_strategies_technological[item].selected_value_aux) / 100 // nd eficiencia deseada
        } else if (
            typeof sub_strategies_value_aux_mod === "boolean" ||
            sub_strategies_value_aux_mod === undefined
        ) {
            sub_strategies_value_aux = sub_strategies_technological[item].np / 100 // nd eficiencia deseada
			np_constant_ = true
        }
        let sub_strategies_nb = parseFloat(sub_strategies_technological[item].nb)
        let sub_strategies_ce_bau = sub_strategies_technological[item].ce_bau.map(
            (ce_bau) => ce_bau * sub_strategies_technological[item].consumption_percent
        )
        ce_bau = sub_strategies_technological[item].ce_bau
        poblacion = sub_strategies_technological[item].poblacion
        pib_billones_usd = sub_strategies_technological[item].PIB_billones_USD
        //utiliza de entrada eficiencia base nb , consumo electico bau ce_bau
        let data_ce = calculateElectricConsumptionEndUse(
            n,
            sub_strategies_value,
            sub_strategies_value_aux,
            sub_strategies_nb,
            sub_strategies_ce_bau,
            sub_strategies_name,
			np_constant_
        )
        let data_ce_without_name = data_ce[1]
        data_model_upgrade.push(data_ce_without_name) //en esta parte en vez de crear un array con los calculos de las 3 equios a BAt
        if (sub_strategies_technological[item].id == "f001") {
            data_upgrade.push(data_ce_without_name)
            let ce_cp = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_c_p
            )
            let ce_i = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_industrial
            )
            let last_value_ce = ce_cp[n - 1] + ce_i[n - 1]
            let last_value_residential = data_upgrade[0][data_upgrade[0].length - 1]
            impact_total_residential_demand = Object.values(last_value_residential)[1] + last_value_ce
            let residential_values = createDataForTospsis(
                impact_total_residential_demand,
                poblacion[n - 1],
                pib_billones_usd[n - 1],
                ce_bau[n - 1],
                sub_strategies_technological[item].name
            )
            data_topsis.push(residential_values)
        } else if (sub_strategies_technological[item].id == "f002") {
            data_upgrade.push(data_ce_without_name)
            let ce_r = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_residential
            )
            let ce_i = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_industrial
            )
            let last_value_ce = ce_r[n - 1] + ce_i[n - 1]
            let last_value_cp = data_upgrade[0][data_upgrade[0].length - 1]
            impact_total_demand_commercial_public = Object.values(last_value_cp)[1] + last_value_ce
            let commercal_public_values = createDataForTospsis(
                impact_total_demand_commercial_public,
                poblacion[n - 1],
                pib_billones_usd[n - 1],
                ce_bau[n - 1],
                sub_strategies_technological[item].name
            )
            data_topsis.push(commercal_public_values)
        } else if (sub_strategies_technological[item].id == "f003") {
            data_upgrade.push(data_ce_without_name)
            let ce_r = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_residential
            )
            let ce_cp = sub_strategies_technological[item].ce_bau.map(
                (ce_bau) => ce_bau * consumption_percent_c_p
            )
            let last_value_ce = ce_r[n - 1] + ce_cp[n - 1]
            let last_value_i = data_upgrade[0][data_upgrade[0].length - 1]
            impact_total_industrial_demand = Object.values(last_value_i)[1] + last_value_ce
            let industrial_values = createDataForTospsis(
                impact_total_industrial_demand,
                poblacion[n - 1],
                pib_billones_usd[n - 1],
                ce_bau[n - 1],
                sub_strategies_technological[item].name
            )
            data_topsis.push(industrial_values)
        }
    }) //elijo el primer bat(residencial y completo con ce proyectado de industrial y comercial y publico y sumo)
    let ce_bau_projected = ce_bau[n - 1]
    let population_projected = poblacion[n - 1]
    let pib_usd_projected = pib_billones_usd[n - 1]
    let impact_consumpt_light_elect_ve = ce_bau_projected + lightweight_sum
    let impact_consumpt_heavy_elect_ve = ce_bau_projected + heavy_sum

    let light_vehicle_values = createDataForTospsis(
        impact_consumpt_light_elect_ve,
        population_projected,
        pib_usd_projected,
        ce_bau_projected,
        "Electrificación del transporte ligero"
    )
    data_topsis.push(light_vehicle_values)

    let heavy_vehicle_values = createDataForTospsis(
        impact_consumpt_heavy_elect_ve,
        population_projected,
        pib_usd_projected,
        ce_bau_projected,
        "Electrificación del transporte carga y pasajeros"
    )
    data_topsis.push(heavy_vehicle_values)
    let total_elect_consump_ev = sumStrategyDatawithAccumulation(data_model_electrification)
    let total_elect_consump_tehn_up = sumStrategyData(data_model_upgrade)
    let total_elect_consump = totalSumStrategyData(total_elect_consump_ev, total_elect_consump_tehn_up)
    createGraphIndicatorEndUse(total_elect_consump, ce_bau, poblacion, pib_billones_usd)
    console.log("data_topsis END", data_topsis)
}

function dataGraphIndicatorsEndUse(strategies) {
    let strategiesModels = strategies.models
    let n_and_year = validateDate()
    let n = n_and_year[0]
    let strategies_array_copia = const_strategies
    let k = 0
    //let strategiesName = getStrategieName()
    let strategies_array_copia_process = filterStrategiesByProcess(strategies_array_copia).models
    for (let i = 0; i < strategies_array_copia_process.length; i++) {
        let process_strategies_name = strategies_array_copia_process[i].name
        try {
            let current_strategies_name = strategiesModels[k].name
            if (process_strategies_name == current_strategies_name) {
                let proccess_strategies = strategies_array_copia_process[i].strategies
                let curren_strategies = strategiesModels[k].strategies
                let l = 0
                for (let j = 0; j < proccess_strategies.length; j++) {
                    let process_strategy_name = proccess_strategies[j].name
                    try {
                        let current_strategy_name = curren_strategies[l].name
                        if (process_strategy_name == current_strategy_name) {
                            let value_new = curren_strategies[l].selected_value
                            let value_aux_new = curren_strategies[l].selected_value_aux
                            proccess_strategies[j].selected_value = value_new
                            proccess_strategies[j].selected_value_aux = value_aux_new
                            l++
                        }
                    } catch (error) {
                        console.log("El índice está fuera del rango de la matriz")
                    }
                }
                k++
            }
        } catch (error) {
            console.log("El índice está fuera del rango de la matriz")
        }
    }
    let electrification_strategies = strategies_array_copia_process[0]
    let technological_upgrade_strategies = strategies_array_copia_process[1]
    generateDataIndicatorEndUse(
        electrification_strategies.strategies,
        technological_upgrade_strategies.strategies,
        n
    )
}

function calculateLossFactor(n, ami, final_reduction, ami_bau, name, type) {
    var data_ami = []
    var data_plot = []
    var data_plot_return = []
    let j = 2
    let factor_perdidas = 0
    let final_reduction_formula = 1 - final_reduction / ami_bau

    if (type == 2){
        //console.log("----progresivo")
        let  ami_progre = ami
        for (m = 0; m< n ; m ++){
            data_ami.push(ami_progre)
            ami_progre = ami_progre * (2/3)
        }
        data_ami.reverse();
    }else {
        //console.log("----lineal")
        var increment_ami = ami / n
        let creaincrement_ami = increment_ami
        for (let a = 0; a < n; a++) {
            data_ami.push(creaincrement_ami)
            creaincrement_ami = creaincrement_ami + increment_ami
        }
    }
    for (let i = 0; i < data_ami.length; i++) {
        let data_plot_dict = {}
        let anio = "202" + j
        if (j > 9) {
            j = 0
            anio = "203" + j
        }
        j++
        factor_perdidas = ami_bau * (1 - data_ami[i] * final_reduction_formula)
        data_plot_dict.Año = anio
        data_plot_dict[name] = factor_perdidas
        data_plot.push(data_plot_dict)
        //ami_bau = factor_perdidas
    }
    data_plot_return["Digitalización y gestión de la medida"] = data_plot
    return [data_plot_return, data_plot]
}

function distributionIndicatorsEEP(fdp, ener_facturada_equ) {
    let name = "Emisiones equivalentes de las pérdidas de distribución"
    let fe = 0.2 //Factor de emisióin [gCO2eq/Wh]
    let eep = 0 // (consumo*fe) /pib
    let anio = ""
    let k = 2
    let data_plot_eep = []
    var data_plot_return = []

    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        let temp = (fdp[i]*ener_facturada_equ[i]/(1-fdp[i]))/1000000
        eep = temp* fe
        data_plot_dict.Año = anio
        data_plot_dict[name] = eep
        data_plot_eep.push(data_plot_dict)
    }
    console.log("data_plot_eep que esta pasando ", data_plot_eep)
    data_plot_return["Indicador emisiones equivalentes de las pérdidas de distribución"] = data_plot_eep
    createChartIndicador3(
        list_name,
        "Indicador emisiones equivalentes de las pérdidas de distribución",
        name,
        data_plot_return,
        "chart_title_7",
        "line-chart-7",
        "graph-container-7"
    )
    return data_plot_return
}

function distributionIndicatorsCEP(fdp, costo_dist, ener_facturada_equ, USD_promedio) {
    let name = "Costo equivalente a pérdidas ADD en Millones de USD"
    let cep = 0 // (consumo /pib)/1000
    let anio = ""
    let k = 2
    let data_plot_cep = []
    var data_plot_return = []
    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        cep = (fdp[i]*ener_facturada_equ[i]/(1 - fdp[i]))*(costo_dist[i]/USD_promedio)
        //data_plot_dict = {"Año": anio, "Indicador costo equivalente a pérdidas": cep};
        data_plot_dict.Año = anio
        data_plot_dict[name] = cep
        data_plot_cep.push(data_plot_dict)
    }
    data_plot_return["Indicador costo equivalente a pérdidas"] = data_plot_cep
    createChartIndicador2(
        list_name,
        "Indicador costo equivalente a pérdidas",
        name,
        data_plot_return,
        "chart_title_6",
        "line-chart-6",
        "graph-container-6"
    )
    return data_plot_return
}

function distributionIndicatorFPD(fdp) {
    let name = "Factor de pérdidas"
    //let eficiency = 0
    let data_plot = []
    let k = 2
    let anio_fdp = ""
    let data_plot_return = []
    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio_fdp = "202" + k
        if (k > 9) {
            k = 0
            anio_fdp = "203" + k
        }
        k++
        //eficiency = generacion[i] / consumo[i]
        data_plot_dict.Año = anio_fdp
        data_plot_dict[name] = fdp[i]
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Indicador de factor de pérdidas"] = data_plot
    createChartIndicador1(
        list_name,
        "Indicador de factor de pérdidas",
        name,
        data_plot_return,
        "chart_title_5",
        "line-chart-5",
        "graph-container-5"
    )
    return data_plot_return
}

function createGraphIndicatorDistribution(fdp) {
    //datos de db desde 2022 hasta 2030, no es necesario agregar año porque el sistem recorre hasta el año que necesita
    //Costo distribución ADD  [$/kWh] [base 2015]
    //Energía Facturada equivalentes ADD  [kW] año
    let costo_dist = [0.1297, 0.1525, 0.1796, 0.2112, 0.2477, 0.2895, 0.3369, 0.3902, 0.4498]
    let ener_facturada_equ = [315764251618.68, 320723989171.48, 325683726724.28, 330643464277.08, 335603201829.88, 340562939382.68, 345522676935.48, 350482414488.28, 355442152041.08]
    let USD_promedio = 2743000000 // factor de conversion
    let fdp_ = distributionIndicatorFPD(fdp)
    let cep = distributionIndicatorsCEP(fdp, costo_dist, ener_facturada_equ, USD_promedio) //Costo equivalente a pérdidas ADD  en Millones de USD [base 2015]
    let eep = distributionIndicatorsEEP(fdp, ener_facturada_equ) //Emisiones equivalentes de las pérdidas de distribución TCO2eq/año

    //select last value for create indicators to save
    let last_fdp_ = Object.values(Object.values(fdp_)[0].at(-1))[1]
    let last_cep = Object.values(Object.values(cep)[0].at(-1))[1]
    let last_eep = Object.values(Object.values(eep)[0].at(-1))[1]

    //array order: enviromental_indicator, economic_indicator, energy_indicator
    for_save_indicators.push(last_eep,last_cep,last_fdp_)

    //lanza topsis, utiliza una variavle global para mantener las difertens strategias, ya que en las
    // graficas de distribucion se promedian
   PrepareDataTopsisDistribution(data_for_topsis_dist)
}

function DataTopsisDistribution(fdp_, cep, eep, name_type_ami) {
    let parent_object = {}
    //let name_type_ami = modifyName(name)
    let fdp_last = Object.values(fdp_)[0].slice(-1)[0]
    let fdp_last_value = Object.values(fdp_last)[1]
    let dfp_last_name = Object.keys(fdp_last)[1]

    let cep_last = Object.values(cep)[0].slice(-1)[0]
    let cep_las_value = Object.values(cep_last)[1]
    let cep_las_name = Object.keys(cep_last)[1]

    let eep_last = Object.values(eep)[0].slice(-1)[0]
    let eep_last_value = Object.values(eep_last)[1]
    let eep_last_name = Object.keys(eep_last)[1]

    let data_topsis_return = Object.assign({}, parent_object, {
        [name_type_ami]: [
            {
                [dfp_last_name]: fdp_last_value,
                [cep_las_name]: cep_las_value,
                [eep_last_name]: eep_last_value,
            },
        ],
    })
    return data_topsis_return
}

function distributionIndicatorFPDToTopsis(fdp) {
    let name = "Factor de pérdidas"
    //let eficiency = 0
    let data_plot = []
    let k = 2
    let anio_fdp = ""
    let data_plot_return = []
    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio_fdp = "202" + k
        if (k > 9) {
            k = 0
            anio_fdp = "203" + k
        }
        k++
        //eficiency = generacion[i] / consumo[i]
        data_plot_dict.Año = anio_fdp
        data_plot_dict[name] = fdp[i]
        data_plot.push(data_plot_dict)
    }
    data_plot_return["Indicador de factor de pérdidas"] = data_plot
    return data_plot_return
}


function distributionIndicatorsCEPtoTopsis(fdp, costo_dist, ener_facturada_equ, USD_promedio) {
    let name = "Costo equivalente a pérdidas ADD en Millones de USD"
    let cep = 0 // (consumo /pib)/1000
    let anio = ""
    let k = 2
    let data_plot_cep = []
    var data_plot_return = []
    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        cep = (fdp[i]*ener_facturada_equ[i]/(1 - fdp[i]))*(costo_dist[i]/USD_promedio)
        //data_plot_dict = {"Año": anio, "Indicador costo equivalente a pérdidas": cep};
        data_plot_dict.Año = anio
        data_plot_dict[name] = cep
        data_plot_cep.push(data_plot_dict)
    }
    data_plot_return["Indicador costo equivalente a pérdidas"] = data_plot_cep
    return data_plot_return
}


function distributionIndicatorsEEPToTopsis(fdp, ener_facturada_equ) {
    let name = "Emisiones equivalentes de las pérdidas de distribución"
    let fe = 0.2 //Factor de emisióin [gCO2eq/Wh]
    let eep = 0 // (consumo*fe) /pib
    let anio = ""
    let k = 2
    let data_plot_eep = []
    var data_plot_return = []

    for (var i = 0; i < fdp.length; i++) {
        let data_plot_dict = {}
        anio = "202" + k
        if (k > 9) {
            k = 0
            anio = "203" + k
        }
        k++
        let temp = (fdp[i]*ener_facturada_equ[i]/(1-fdp[i]))/1000000
        eep = temp* fe
        data_plot_dict.Año = anio
        data_plot_dict[name] = eep
        data_plot_eep.push(data_plot_dict)
    }
    data_plot_return["Indicador emisiones equivalentes de las pérdidas de distribución"] = data_plot_eep
    return data_plot_return
}

function PrepareDataTopsisDistribution(data) {
    //datos de db desde 2022 hasta 2030, no es necesario agregar año porque el sistem recorre hasta el año que necesita
    //Costo distribución ADD  [$/kWh] [base 2015]
    //Energía Facturada equivalentes ADD  [kW] año
    console.log("data_topsis DIST", data_topsis)
    data_topsis = []
    let costo_dist = [0.1297, 0.1525, 0.1796, 0.2112, 0.2477, 0.2895, 0.3369, 0.3902, 0.4498]
    let ener_facturada_equ = [315764251618.68, 320723989171.48, 325683726724.28, 330643464277.08, 335603201829.88, 340562939382.68, 345522676935.48, 350482414488.28, 355442152041.08]

    let USD_promedio = 2743000000 // factor de conversion
    for (let array of data){
        let a_data = []
        let name
        for (let array2 of array) {
            a_data.push(Object.values(array2)[1])
            name = Object.keys(array2)[1]
        }
        let fdp_ = distributionIndicatorFPDToTopsis(a_data)
        let cep = distributionIndicatorsCEPtoTopsis(a_data, costo_dist, ener_facturada_equ, USD_promedio) //Costo equivalente a pérdidas ADD  en Millones de USD [base 2015]
        let eep = distributionIndicatorsEEPToTopsis(a_data, ener_facturada_equ) //Emisiones equivalentes de las pérdidas de distribución TCO2eq/año
        let values = DataTopsisDistribution(fdp_, cep, eep, name)
        data_topsis.push(values)
    }
    console.log("data_topsis DIST", data_topsis)
}

let average_loss_factor
function decentralizationAndDigitizationStrategies(sub_strategies, n, strategies_name) {
    //console.log("-----decentralizationAndDigitizationStrategies ---  ")
    let sub_strategies_key = Object.keys(sub_strategies)
    let loss_factor_total = []
    data_for_topsis_dist = []
    sub_strategies_key.forEach(function (item, index) {
        //utiliza de entrada rficirencia base nb , consumo electico bau ce_bau
        let sub_strategies_name = sub_strategies[item].name
        let sub_strategies_type = sub_strategies[item].type
        let sub_strategies_value = parseFloat(sub_strategies[item].selected_value) / 100 // porcentaje de incorporacion ami
        let sub_strategies_value_aux_mod = sub_strategies[item].selected_value_aux
        let sub_strategies_value_aux
        if (typeof sub_strategies_value_aux_mod === "string") {
            sub_strategies_value_aux = parseFloat(sub_strategies[item].selected_value_aux) / 100 // reduccion final dada por el usuario
        } else if (typeof sub_strategies_value_aux_mod === "boolean") {
            sub_strategies_value_aux = parseFloat(sub_strategies[item].final_reduction_bau) // reduccion final por defecto
        }
        let sub_strategies_ami_bau = parseFloat(sub_strategies[item].ami_bau)
        let data_ce_consumpt = calculateLossFactor(
            n,
            sub_strategies_value,
            sub_strategies_value_aux,
            sub_strategies_ami_bau,
            sub_strategies_name,
            sub_strategies_type
        )
        let data_ce = data_ce_consumpt[0]
        const_loss_factor = data_ce_consumpt[1]
        let array_data = []
        //loss_factor_total.push(const_loss_factor)
        for (let array of const_loss_factor) {
            array_data.push(Object.values(array)[1])
        }
        loss_factor_total.push(array_data)
        data_for_topsis_dist.push(const_loss_factor)
        console.log("loss_factor_total ", loss_factor_total)
        console.log("data_for_topsis_dist ", data_for_topsis_dist)
        createChartUpgrade(
            list_name,
            strategies_name,
            sub_strategies_name,
            data_ce,
            "chart_title_4",
            "line-chart-4",
            "graph-container-4"
        )
    })
    average_loss_factor = promedioElemento(loss_factor_total);
    //console.log("data_for_topsis_dist ", data_for_topsis_dist)
    console.log("average_loss_factor ", average_loss_factor)
    //createGraphIndicatorDistribution(average_loss_factor)
    //PrepareDataTopsisDistribution(data_for_topsis_dist)
}

function promedioElemento(arrays) {
    let resultado = [];
    let longitud = arrays[0].length;
    for (let i = 0; i < longitud; i++) {
        let suma = 0;
        for (let array of arrays) {
            suma += array[i];
        }
        resultado.push(suma / arrays.length);
    }
    return resultado;
}

function dataGraphStrategiesDistribution(strategies) {
    //console.log(" --- dataGraphStrategiesDistribution --- ")
    let strategiesModels = strategies.models
    let n_and_year = validateDate()
    let n = n_and_year[0]
    //let strategiesName = getStrategieName()
    let strategiesModelsKeys = Object.keys(strategiesModels)
    strategiesModelsKeys.forEach(function (items, index) {
        let strategies_name = strategiesModels[items].name
        let sub_strategies = strategiesModels[items].strategies
        decentralizationAndDigitizationStrategies(sub_strategies, n, strategies_name)
    })
}

function updateChart(strategies_array) {
    let current_values = getCurrentValues()
    let current_values_sliders = current_values[0]
    let current_values_text = current_values[1]
    strategies_const = filterStrategiesByIdValues(
        strategies_array,
        current_values_sliders,
        current_values_text
    )
    let proccess = getProcessName()
    if (proccess == "generation") {
        plotDataStrategies(strategies_const)
    } else if (proccess == "distribution") {
        dataGraphStrategiesDistribution(strategies_const)
    } else if (proccess == "end_use") {
        dataGraphStrategiesEndUse(strategies_const)
    }
}

document.getElementById("adjust_sub_estrategies_next").addEventListener("click", function () {
    let proccess = getProcessName()
    if (proccess == "generation") {
        data_topsis = []
        plotDataIndicators(strategies_const)
    } else if (proccess == "distribution") {
        createGraphIndicatorDistribution(average_loss_factor)
    } else if (proccess == "end_use") {
        dataGraphIndicatorsEndUse(strategies_const)
    }
})

function topsisValues(weights) {
    let parent_object = {}
    // let criterios_values = Object.assign({}, parent_object, {
    // 	criteria_values: [
    // 		{ energetico: 0.352350155182091, economico: 0.138435264150802, ambiental: 0.509214580667107 },
    // 	],
    // })
    let criterios_values = {}
    criterios_values = Object.assign({}, parent_object, {
        criteria_values: [weights],
    })
    console.log("data_topsis LAST: ",data_topsis)
    data_topsis.push(criterios_values)
    const dict_values = {data_topsis}
    const s = JSON.stringify(dict_values)
    //console.log(s)
    $.ajax({
        url: "/dashboard/analysis",
        type: "POST",
        contentType: "application/json",
        charset: "utf-8",
        data: JSON.stringify(s),
        success: function (data, status, xhr) {
            // success callback function
            console.log("status: " + status)
            //console.log("data: " ,data)
            createDataChartTopsis(data)
            data_topsis.pop()
        },
        error: function (jqXhr, textStatus, errorMessage) {
            // error callback
            console.log("Error: " + errorMessage)
        },
    })
}

function editDataStrategy(strategies_const, id){
    let all_data = generateDataToSave(strategies_const)
    let datos = new FormData();

    datos.append("id", id)
    datos.append("all_data", JSON.stringify(all_data))
    datos.append("data_indicators", JSON.stringify(for_save_indicators))

    fetch("/dashboard/editData", {
        method: "POST",
        body: datos
    })
    .then(respuesta => respuesta.json())
    .then(json => {
        console.log(json);
        all_data = [];
        for_save_indicators = [];
    })
    .catch(error => {
        console.log(error);
    })
}

function generateDataToSave(strategies_const){
    let all_data = []
    for (var i = 0; i< strategies_const.models.length; i ++){
        let id_strategy = strategies_const.models[i].id
        for ( var j = 0; j < strategies_const.models[i].strategies.length; j ++){
            let data = {}
            let id_sub_strategy =  strategies_const.models[i].strategies[j].id
            let value =  strategies_const.models[i].strategies[j].selected_value
            let value_aux =  strategies_const.models[i].strategies[j].selected_value_aux
            data["id_strategy"] = id_strategy
            data["id_sub_strategy"] = id_sub_strategy
            data["value"] = value
            data["value_aux"] = value_aux //(nuevoValor === 0) ? "valor por defecto" : nuevoValor;
            all_data.push(data)
            //console.log("strategies_const. all_data " ,all_data);
        }
    }
    //console.log("strategies_const. all_data 2" ,all_data);
    return all_data
}

function saveDataStrategy(strategies_const){
    let all_data = generateDataToSave(strategies_const)
    let datos = new FormData();
    let id_user = "alex"
    let strategy_name = document.getElementById("name-input").value
    let type = $("#process-selected").find("span").text()
    let n_and_year = validateDate()
    let anio = n_and_year[1]

    datos.append("user", id_user)
    datos.append("strategy_name", strategy_name)
    datos.append("type", type)
    datos.append("año", anio)
    datos.append("all_data", JSON.stringify(all_data))
    datos.append("data_indicators", JSON.stringify(for_save_indicators))

    fetch("/auth/saveData", {
        method: "POST",
        body: datos
    })
    .then(respuesta => respuesta.json())
    .then(json => {
        console.log(json);
        all_data = []
        for_save_indicators = []
    })
    .catch(error => {
        console.log(error);
    })
}

function getProcessName2(processName) {
    if (processName == "Generación") {
        processName = "generation"
    } else if (processName == "Distribución") {
        processName = "distribution"
    } else if (processName == "Uso final") {
        processName = "end_use"
    }
    return processName
}

function filterStrategiesByIdValuesFromEdit(array, idsValues, idsValuesText, year) {
    let ids = Object.keys(idsValues)
    let exist = false
    //console.log("--- filterStrategiesByIdValues ---")
    if (Object.keys(idsValuesText).length > 0) {
        exist = true
    }
    let new_array = array.models
        .filter((model) => model.strategies.some((strategy) => ids.includes(strategy.id)))
        .map((model) => {
            let newElt
            if (exist) {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue = Object.assign({}, inStrategies, {
                                year: year,
                                value: idsValues[ids.find((strategiId) => strategiId == inStrategies.id)],
                                value_aux:
                                    idsValuesText[ids.find((strategiId) => strategiId == inStrategies.id)],
                            })
                            return newEltValue
                        }),
                })
            } else {
                newElt = Object.assign({}, model, {
                    strategies: model.strategies
                        .filter((strategy) => ids.includes(strategy.id))
                        .map((inStrategies) => {
                            let newEltValue = Object.assign({}, inStrategies, {
                                year: year,
                                value: idsValues[ids.find((strategiId) => strategiId == inStrategies.id)],
                            })
                            return newEltValue
                        }),
                })
            }
            return newElt
        })
    array.models = new_array
    return array
}

function set(){
    $("#adjust_sub_estrategies_prev").addClass("btn-danger")
}

function lanzarEdit(strategies_array_edit) {
    let button = document.getElementById("adjust_sub_estrategies_prev");
    button.addEventListener("click", set)
    //boton.setAttribute("disabled", "true");
    //$("#adjust_sub_estrategies_prev").addClass("btn-danger")

    // $("#adjust_sub_estrategies_prev").addClass("btn-danger")
    let div = document.getElementById("prueba");
    div.style.display = "none";
    let div2 = document.getElementById("guardar");
    div2.style.display = "none";

    ActiveSection("scenarios_3")
    var parent = document.getElementById("template_strategies").cloneNode(true)
    parent.querySelector("#process").innerHTML = strategies_array_edit.process
    strategies_array_edit.models.forEach((model) => {
        var model_html = loadModel(model, parent)
        model.strategies.forEach((strategy) => {
            model_html
                .querySelector("#strategies-model-id")
                .appendChild(loadStrategy(strategy, model_html, model.id))
        })
        model_html.querySelector("#strategies-model-id").id = "strategies-model-" + model.id
        /* model_html.querySelector("#strategies-model-id").id = "strategies-model-" + model.id */
        parent.querySelector("#accordion-strategies").appendChild(model_html)
    })
    document.getElementById("test-clone").innerHTML = ""
    document.getElementById("test-clone").appendChild(parent)
    removeSliders()
    loadSliders(strategies_array_edit)
    loadInputsAux(strategies_array_edit)
    updateChart(strategies_array_edit)
}

function viewScenary(id, scenary_name, proccess, year) {
    console.log("id " + id + " scenary_name " + scenary_name + " proccess " + proccess + " year " + year)
    id_edit = id
    //set initial variables
    SetSelectName("process-selected", getProcessName2(proccess))
    document.getElementById("fecha").innerHTML = String(year)
    document.getElementById("fecha").value = String(year)
    loadParameters(scenary_name, proccess, year)

    fetch(`/dashboard/edit_scenary?id=${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta');
            }
            return response.json();
        })
        .then(data => {
            console.log(" response", data)
            let objeto_values = data.reduce((acc, elem) => {
                acc[elem.id_sub_strategy] = elem.value;
                return acc;
            }, {});

            let objeto_values_aux = data.reduce((acc, elem) => {
                if (elem.value_aux != null) {
                    acc[elem.id_sub_strategy] = elem.value_aux;
                }
                return acc;
            }, {});
            const_strategies = JSON.parse(JSON.stringify(strategies_to_load_edit))
            loadUnit(units)
            let strategies_array_edit = filterStrategiesByProcess(strategies_to_load_edit)
            strategies_to_show = filterStrategiesByIdValuesFromEdit(strategies_array_edit, objeto_values, objeto_values_aux, year)
            lanzarEdit(strategies_array_edit)
        })
        .catch(error => console.error(error));
}

//comparate scenary
function buscarObjetosPorIds(ids, arregloDeObjetos) {
    return arregloDeObjetos.filter(objeto => ids.includes(objeto.id));
}

function prepareDataTopsisFromScenerios(data_table_init, arr_ids) {
    console.log("---prepareDataTopsisFromScenerios---")
    console.log("data_table_init",data_table_init)
    console.log("arr_ids",arr_ids)

    // data_table_init.forEach(element => {
        
    //     console.log(element)
    // })
    let ids = arr_ids.map( ids => parseInt(ids))
    console.log("ids",ids)
    let strategies = buscarObjetosPorIds(ids, data_table_init);
    console.log("strategies",strategies)

    let data_topsis_return =[]
    let parent_object = {}
    strategies.forEach(strategy => {
        let data_topsis_ = Object.assign({}, parent_object, {
            [strategy.strategy_name]: [
                {
                    ["economico"]: strategy.economic_indicator,
                    ["energetico"]: strategy.energy_indicator,
                    ["ambiental"]: strategy.environmental_indicator,
                },
            ],
        })
        data_topsis.push(data_topsis_)
    })
    //
    // // let name_plant = modifyName(name)
    // // let efi = Object.values(eficiency)[0].slice(-1)[0]
    // // let efi_last_value = Object.values(efi)[1]
    // // let efi_last_name = Object.keys(efi)[1]

    // console.log("efi",efi)
    // console.log("efi_last_value",efi_last_value)
    // console.log("efi_last_name",efi_last_name)

    // // let iep_last = Object.values(iep)[0].slice(-1)[0]
    // // let iep_las_value = Object.values(iep_last)[1]
    // // let iep_las_name = Object.keys(iep_last)[1]

    // // let iec_last = Object.values(iec)[0].slice(-1)[0]
    // // let iec_last_value = Object.values(iec_last)[1]
    // // let iec_last_name = Object.keys(iec_last)[1]


    console.log("data_topsis SAVE",data_topsis)
    // return data_topsis_return
}

/* Desarrollo Nuevo */
$(".btn-progress-next").on("click", function () {
    var currentStepNum = $(".checkout-progress").data("current-step")
    var nextStepNum = currentStepNum + 1
    var currentStep = $(".stepp.stepp-" + currentStepNum)
    var nextStep = $(".stepp.stepp-" + nextStepNum)
    var currentProgress = $(".checkout-progress")
    if (currentStepNum == 6) {
        return false
    }
    currentProgress.removeClass(".stepp-" + currentStepNum).addClass(".stepp-" + (currentStepNum + 1))

    currentStep.removeClass("active").addClass("valid")
    currentStep.find("span").addClass("opaque")
    currentStep.find(".fa.fa-check").removeClass("opaque")

    nextStep.addClass("active")

    currentProgress
        .removeAttr("class")
        .addClass("checkout-progress stepp-" + nextStepNum)
        .data("current-step", nextStepNum)
})

$(".btn-progress-prev").on("click", function () {
    var currentStepNum = $(".checkout-progress").data("current-step")
    var prevStepNum = currentStepNum - 1
    var currentStep = $(".stepp.stepp-" + currentStepNum)
    var prevStep = $(".stepp.stepp-" + prevStepNum)
    var currentProgress = $(".checkout-progress")
    if (currentStepNum == 1) {
        return false
    }
    currentProgress.removeClass(".stepp-" + currentStepNum).addClass(".stepp-" + prevStepNum)

    currentStep.removeClass("active")

    prevStep.find("span").removeClass("opaque")
    prevStep.find(".fa.fa-check").addClass("opaque")
    prevStep.addClass("active").removeClass("valid")

    currentProgress
        .removeAttr("class")
        .addClass("checkout-progress stepp-" + prevStepNum)
        .data("current-step", prevStepNum)
})

$(".weight-input").each(function () {
    $(this).on("change", {passive: true}, function (changeEvt) {
        if (!sum_values_checker()) {
            $(this).addClass("is-invalid")
            document.getElementById("topsis-start").classList.add("disabled")
        } else {
            $(".weight-input").removeClass("is-invalid")
            document.getElementById("topsis-start").classList.remove("disabled")
        }
    })
})

function get_weights_values() {
    let values = $(".weight-input")
        .map(function () {
            return parseFloat($(this).val())
        })
        .get()
    return values
}

function sum_values_checker() {
    let sum = get_weights_values().reduce((partialSum, a) => partialSum + a, 0)
    return sum < 99 || sum > 100 ? false : true
}

function weights_check() {
    let weights = {
        energetico: 0.35,
        economico: 0.23,
        ambiental: 0.40,
    }

    if (sum_values_checker()) {
        let values = get_weights_values()
        weights["ambiental"] = values[0] / 100
        weights["economico"] = values[1] / 100
        weights["energetico"] = values[2] / 100
        topsisValues(weights)
    } else {
        console.log("error de valores")
    }
}

//# sourceMappingURL=dashboard.js.map