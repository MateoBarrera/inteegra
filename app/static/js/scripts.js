/*!
 * Start Bootstrap - Scrolling Nav v5.0.2 (https://startbootstrap.com/template/scrolling-nav)
 * Copyright 2013-2021 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-scrolling-nav/blob/master/LICENSE)
 */
//
// Scripts
//

window.addEventListener("DOMContentLoaded", (event) => {
    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector("#mainNav")
    if (mainNav) {
        try{
            new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 24,
            });
        } catch (e){

        }

    }

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector(".navbar-toggler")
    const responsiveNavItems = [].slice.call(document.querySelectorAll("#navbarResponsive .nav-link"))
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener("click", () => {
            if (window.getComputedStyle(navbarToggler).display !== "none") {
                navbarToggler.click()
            }
        })
    })
})

function ActivateLink(section) {
    document.getElementById("I-" + section).setAttribute("class", "nav-item active")
}

let preSectionId = "main";

function ActiveSection(sectionId) {
    if (sectionId !== preSectionId) {
        document.getElementById(preSectionId).hidden = true
        document.getElementById(sectionId).hidden = false
        preSectionId = sectionId
    }
}

function SetSelectName(button, list_name) {
    let select_name
    if (list_name === "generation") {
        select_name = "Generación"
    } else if (list_name === "distribution") {
        select_name = "Distribución"
    } else if (list_name === "end_use") {
        select_name = "Uso final"
    } else if (list_name === "Agregados") {
        select_name = "Agregados"
    } else {
        select_name = "Desagregados"
    }
    document.getElementById(button).firstElementChild.innerHTML = select_name
}

const datatable_config = {
    language: {
        url: "//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json",
    },
    ordering: false,
    hover: true,
    filter: false,
    responsive: true,
    pageLength: 200,
    scrollResize: true,
    scrollX: false,
    scrollY: true,
    scrollCollapse: false,
    dom: "Bfrtip",
    aaSorting: [],
    info: false,
    deferRender: true,
    paging: false,
    buttons: ["copyHtml5", "excelHtml5", "csvHtml5", "pdfHtml5"],
};

// Test code
$(".progress").each(function (_, progress) {
    var steps = $("> div.right > div", progress)
    steps.each(function (i, el) {
        return $(el).mouseenter(function (e) {
            return onHover(el)
        })
    })
    var onHover = function (el) {
        steps.removeClass(["current", "prev"])
        el.classList.add("current")
        $(el).prevAll().slice(1).addClass("prev")
    }
})


