var activateNavbarItem = function(elementId) {
  var activeItem = $("#navbarItemList").children("li.active");
  var targetItem = $(elementId);
  activeItem.removeClass("active");
  targetItem.addClass("active");
};

var hideContent = function() {
  $(".necco-content").css("display", "none");
  $(".overlay").css("display", "");
  $(".loading").css("display", "");
};

var showContent = function(idContent) {
  $(".necco-content").css("display", "none");
  $(".overlay").fadeOut();
  $(".loading").fadeOut();
  $(idContent).fadeIn();
};

var prepareContent = function(type_) {
  activateNavbarItem("#navbarItem" + type_);
  showContent("#content" + type_);

  var content = $("#content" + type_);
  content.empty();

  var table = $("<table>").appendTo(content);
  table.addClass("table");
  table.addClass("table-responsive");
  table.addClass("table-hover");

  return table;
};

var sortRecordsByKana = function(records) {
  return records.sort(
    function(first, second) {
      if(first.kana > second.kana) { return 1; }
      else if(first.kana < second.kana) { return -1; }
      else { return 0; }
    })
};

$(function() {
  $("#navbarItemPassbook").on("click", function() {
    hideContent();
    activateNavbarItem("#navbarItemPassbook");
    showContent("#contentPassbook");
  });

  $("#navbarItemSettings").on("click", function() {
    hideContent();
    activateNavbarItem("#navbarItemSettings");

    $.ajax({
      type: "GET",
      url: "/api/account",
      dataType: "json"
    }).done(function(data, text, jqxhr){
      for(var key in data){
        $("#" + key).val(data[key]);
      }
      showContent("#contentSettings");
    }).fail(function(jqxhr, text, error){
      showContent("#contentSettings");
    });
  });

  $("#buttonUpdateAccount").on("click", function() {
    var sending_data = $("#formAccount").serializeArray();
    //var ret = $.ajax({
    //  type: "POST",
    //  url: "/api/account",
    //  dataType: "json",
    //  data: "",
    //});
  });

  $("#navbarItemAbilities").on("click", function() {
    hideContent();

    var type_ = "Abilities";
    var table = prepareContent(type_);

    // TODO: columnsもGETするように
    columns = new Array("name", "kana", "detail");
    columns_j = new Array("名前", "よみ", "できること");

    var head = $("<thead>").appendTo(table);
    var tr = $("<tr>").appendTo(head);
    for(var i = 0; i <= columns_j.length; i++) {
      $("<th>").text(columns_j[i]).appendTo(tr)
    }

    $.ajax({
      type: "GET",
      url: "/api/" + type_.toLowerCase(),
      dataType: "json"
    }).done(function(data, text, jqxhr){
      var length = data.length;
      var records = sortRecordsByKana(data.body);
      var body = $("<tbody>").appendTo(table);

      for(var record of records) {
        var tr = $("<tr>").appendTo(body);
        for(var i = 0; i <= columns.length; i++) {
          $("<td>").text(record[columns[i]]).appendTo(tr);
        }
      }

      showContent("#contentAbilities");
    }).fail(function(jqxhr, text, error){
      showContent("#contentAbilities");
    });
  });

  $("#navbarItemRequests").on("click", function() {
    hideContent();

    var type_ = "Requests";
    var table = prepareContent(type_);

    // TODO: columnsもGETするように
    columns = new Array("name", "kana", "detail");
    columns_j = new Array("名前", "よみ", "してほしいこと");

    var head = $("<thead>").appendTo(table);
    var tr = $("<tr>").appendTo(head);
    for(var i = 0; i <= columns_j.length; i++) {
      $("<th>").text(columns_j[i]).appendTo(tr)
    }

    $.ajax({
      type: "GET",
      url: "/api/" + type_.toLowerCase(),
      dataType: "json"
    }).done(function(data, text, jqxhr){
      var length = data.length;
      var records = sortRecordsByKana(data.body);
      var body = $("<tbody>").appendTo(table);

      for(var record of records) {
        var tr = $("<tr>").appendTo(body);
        for(var i = 0; i <= columns.length; i++) {
          $("<td>").text(record[columns[i]]).appendTo(tr);
        }
      }

      showContent("#id-necco-content-requests");
    }).fail(function(jqxhr, text, error){
      showContent("#id-necco-content-requests");
    });
  });
});

$(window).on("load", function() {
  hideContent();
  $("#navbarItemPassbook").addClass("active");
  showContent("#contentPassbook");
});
