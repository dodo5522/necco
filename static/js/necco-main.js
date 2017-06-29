$(document).ready(function(){
  $("#navbarItemPassbook").on("click", function() {
    hideContent();
    activateNavbarItem("#navbarItemPassbook");
    showContent("#contentPassbook");
  });

  $("#navbarItemAbilities").on("click", function() {
    hideContent();

    var type_ = "Abilities";
    var table = prepareContent(type_);

    $.ajax({
      type: "GET",
      url: "/api/" + type_.toLowerCase(),
      dataType: "json"
    }).done(function(data, text, jqxhr){
      var length = data.length;
      var columns = data.columns
      var records = sortRecordsByKana(data.body);

      var body = $("<tbody>").appendTo(table);
      var head = $("<thead>").appendTo(table);
      var tr = $("<tr>").appendTo(head);

      for(var i = 0; i < columns.length; i++) {
        $("<th>").text(columns[i]).appendTo(tr)
      }

      for(var i = 0; i < records.length; i++) {
        var tr = $("<tr>").appendTo(body);
        for(var j = 0; j <= columns.length; j++) {
          $("<td>").text(records[i][columns[j]]).appendTo(tr);
        }
      }

      showContent("#content" + type_);
    }).fail(function(jqxhr, text, error){
      showContent("#content" + type_);
    });
  });

  $("#navbarItemRequests").on("click", function() {
    hideContent();

    var type_ = "Requests";
    var table = prepareContent(type_);

    $.ajax({
      type: "GET",
      url: "/api/" + type_.toLowerCase(),
      dataType: "json"
    }).done(function(data, text, jqxhr){
      var length = data.length;
      var columns = data.columns
      var records = sortRecordsByKana(data.body);

      var body = $("<tbody>").appendTo(table);
      var head = $("<thead>").appendTo(table);
      var tr = $("<tr>").appendTo(head);

      for(var i = 0; i < columns.length; i++) {
        $("<th>").text(columns[i]).appendTo(tr)
      }

      for(var i = 0; i < records.length; i++) {
        var tr = $("<tr>").appendTo(body);
        for(var j = 0; j <= columns.length; j++) {
          $("<td>").text(records[i][columns[j]]).appendTo(tr);
        }
      }

      showContent("#content" + type_);
    }).fail(function(jqxhr, text, error){
      showContent("#content" + type_);
    });
  });

  hideContent();
  activateNavbarItem("#navbarItemPassbook");
  showContent("#contentPassbook");
});
