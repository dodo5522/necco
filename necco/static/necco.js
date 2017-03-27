$(function() {
  var activateNavbarItem = function(elementId) {
    var activeItem = $("#navbar-item-list").children("li.active");
    var targetItem = $(elementId);
    activeItem.removeClass("active");
    targetItem.addClass("active");
  };

  var showContent = function(idContent) {
    $(".necco-content").css("display", "none");
    $(idContent).css("display", "");
  };

  $("#navbar-item-passbook").on("click", function() {
    activateNavbarItem("#navbar-item-passbook");
    showContent("#id-necco-content-passbook");
  });
  $("#navbar-item-settings").on("click", function() {
    activateNavbarItem("#navbar-item-settings");
    showContent("#id-necco-content-settings");
  });
  $("#navbar-item-deshilist").on("click", function() {
    activateNavbarItem("#navbar-item-deshilist");
    showContent("#id-necco-content-deshilist");

    var abilities;
    var res = $.ajax({
      type: "GET",
      url: "/api/ability-list",
      dataType: "json"});

    if(res.status === 200) {
      abilities = JSON.parse(res.responseText);

      var content = $("#id-necco-content-deshilist");
      content.empty();

      var table = $("<table>").appendTo(content);
      table.addClass("table");
      table.addClass("table-responsive");
      table.addClass("table-hover");

      columns = new Array("name", "kana", "detail");
      columns_j = new Array("名前", "よみ", "できること");

      var head = $("<thead>").appendTo(table);
      var tr = $("<tr>").appendTo(head);
      for(var i = 0; i <= columns_j.length; i++) {
        $("<th>").text(columns_j[i]).appendTo(tr)
      }

      var body = $("<tbody>").appendTo(table);
      for(var ability of abilities) {
        var tr = $("<tr>").appendTo(head);
        for(var i = 0; i <= columns.length; i++) {
          $("<td>").text(ability[columns[i]]).appendTo(tr);
        }
      }
    }
  });

  $("#navbar-item-passbook").addClass("active");
});
