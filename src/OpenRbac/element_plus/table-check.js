/* Check every row box in this table.
   requirement-html-javascript — /table-check.js.
   The header box has no name, so it is not posted.
   This file does not read layout and does not write a height.
*/
(function () {
  "use strict";

  function rowBoxes(table) {
    return table.querySelectorAll('tbody input.table-check[type="checkbox"]');
  }

  function headerBox(table) {
    return table.querySelector('thead input.table-check[type="checkbox"]');
  }

  function paintHeader(table) {
    var head = headerBox(table);
    if (!head) {
      return;
    }
    var list = rowBoxes(table);
    var marked = 0;
    var index;
    for (index = 0; index < list.length; index += 1) {
      if (list[index].checked) {
        marked += 1;
      }
    }
    head.checked = list.length > 0 && marked === list.length;
    head.indeterminate = marked > 0 && marked < list.length;
  }

  document.addEventListener("change", function (event) {
    var box = event.target;
    if (!box || box.nodeName !== "INPUT" || box.type !== "checkbox") {
      return;
    }
    if (!box.classList || !box.classList.contains("table-check")) {
      return;
    }
    var table = box.closest("table");
    if (!table) {
      return;
    }
    if (box.closest("thead")) {
      var list = rowBoxes(table);
      var index;
      for (index = 0; index < list.length; index += 1) {
        list[index].checked = box.checked;
      }
      box.indeterminate = false;
      return;
    }
    paintHeader(table);
  });
})();
