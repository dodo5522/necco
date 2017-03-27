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

  var getSortedDeshiRecords = function(type_) {
    var records;
    var res = $.ajax({
      type: "GET",
      url: "/api/" + type_,
      dataType: "json"});

    if(res.status === 200) {
      records = res.responseJSON.sort(
        function(first, second) {
          if(first.kana > second.kana) {
            return 1;
          }
          else if(first.kana < second.kana) {
            return -1;
          }
          else {
            return 0;
          }
        })

    return records;
  };

  $("#navbar-item-abilities").on("click", function() {
    var type_ = "abilities";

    activateNavbarItem("#navbar-item-" + type_);
    showContent("#id-necco-content-" + type_);

    var content = $("#id-necco-content-" + type_);
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

    var records = getSortedDeshiRecords(type_);

    var body = $("<tbody>").appendTo(table);
    for(var record of records) {
      var tr = $("<tr>").appendTo(head);
      for(var i = 0; i <= columns.length; i++) {
        $("<td>").text(record[columns[i]]).appendTo(tr);
      }
    }
  });

  $("#navbar-item-requests").on("click", function() {
    var type_ = "requests";

    activateNavbarItem("#navbar-item-" + type_);
    showContent("#id-necco-content-" + type_);

    var type_ = "requests";
    var content = $("#id-necco-content-" + type_);
    content.empty();

    var table = $("<table>").appendTo(content);
    table.addClass("table");
    table.addClass("table-responsive");
    table.addClass("table-hover");

    columns = new Array("name", "kana", "detail");
    columns_j = new Array("名前", "よみ", "してほしいこと");

    var head = $("<thead>").appendTo(table);
    var tr = $("<tr>").appendTo(head);
    for(var i = 0; i <= columns_j.length; i++) {
      $("<th>").text(columns_j[i]).appendTo(tr)
    }

    var records = getSortedDeshiRecords(type_);

    var body = $("<tbody>").appendTo(table);
    for(var record of records) {
      var tr = $("<tr>").appendTo(head);
      for(var i = 0; i <= columns.length; i++) {
        $("<td>").text(record[columns[i]]).appendTo(tr);
      }
    }
  });

  $("#navbar-item-passbook").addClass("active");
});
