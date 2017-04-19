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

var prepareContent = function(type_) {
  activateNavbarItem("#navbar-item-" + type_);
  showContent("#id-necco-content-" + type_);

  var content = $("#id-necco-content-" + type_);
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
  $("#navbar-item-passbook").on("click", function() {
    activateNavbarItem("#navbar-item-passbook");
    showContent("#id-necco-content-passbook");
  });

  $("#navbar-item-settings").on("click", function() {
    activateNavbarItem("#navbar-item-settings");

    $.ajax({
      type: "GET",
      url: "/api/account",
      dataType: "json"
    }).done(function(data, text, jqxhr){
      $("#name1").val(data["Profile.name_"].split(" ")[0]);
      $("#name2").val(data["Profile.name_"].split(" ")[1]);
      $("#kana1").val(data["Profile.kana"].split(" ")[0]);
      $("#kana2").val(data["Profile.kana"].split(" ")[1]);
      $("#nickname").val(data["Profile.nickname"]);
      $("#email").val(data["User.email"]);
      $("#pref").val(data["Prefecture.name_"]);
      $("#addr1").val(data["Profile.city"]);
      $("#longitude").val(data["Profile.longitude"]);
      $("#latitude").val(data["Profile.latitude"]);
      $("#tel1").val(data["Profile.phone"].split("-")[0]);
      $("#tel2").val(data["Profile.phone"].split("-")[1]);
      $("#tel3").val(data["Profile.phone"].split("-")[2]);
      $("#fax1").val(data["Profile.fax"].split("-")[0]);
      $("#fax2").val(data["Profile.fax"].split("-")[1]);
      $("#fax3").val(data["Profile.fax"].split("-")[2]);
    }).fail(function(jqxhr, text, error){
    });

    showContent("#id-necco-content-settings");
  });

  $("#navbar-item-abilities").on("click", function() {
    var type_ = "abilities";
    var table = prepareContent(type_);

    columns = new Array("name", "kana", "detail");
    columns_j = new Array("名前", "よみ", "できること");

    var head = $("<thead>").appendTo(table);
    var tr = $("<tr>").appendTo(head);
    for(var i = 0; i <= columns_j.length; i++) {
      $("<th>").text(columns_j[i]).appendTo(tr)
    }

    $.ajax({
      type: "GET",
      url: "/api/" + type_,
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
    }).fail(function(jqxhr, text, error){
    });
  });

  $("#navbar-item-requests").on("click", function() {
    var type_ = "requests";
    var table = prepareContent(type_);

    columns = new Array("name", "kana", "detail");
    columns_j = new Array("名前", "よみ", "してほしいこと");

    var head = $("<thead>").appendTo(table);
    var tr = $("<tr>").appendTo(head);
    for(var i = 0; i <= columns_j.length; i++) {
      $("<th>").text(columns_j[i]).appendTo(tr)
    }

    $.ajax({
      type: "GET",
      url: "/api/" + type_,
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
    }).fail(function(jqxhr, text, error){
    });
  });

  });

  $("#navbar-item-passbook").addClass("active");
});
