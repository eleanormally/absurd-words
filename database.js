APIURI = "https://absurdwordsbackend.herokuapp.com/";

$(document).ready(function() {

    getBaseTable();

    $("#logScore").change(function(){
        ischecked = $(this).is(':checked');
        if(ischecked){
            $(".scoreValue").each(function(){
                $(this).html(Math.round(Math.exp((Number($(this).text())))));
            });
        }
        else {
            $(".scoreValue").each(function(){
                $(this).html(Math.log((Number($(this).text()))).toFixed(5));
            });
        }
    });

    $(".searchBox").on('keypress', function (e) {
        if(e.which === 13) {
            search($(this).val());
        }
    });

});

function search(word) {
    $.get(APIURI + "/getWord/" + word.toLowerCase() + "?calculate=true", function(data){
        if (data.hasOwnProperty("word")) {
            if($(".showTable").is(":hidden")) {
                $("#wordTable > tbody").empty();
            }
            row = $(".wordTableBody").append("<tr class=\"wordRow\"></tr>");
            row.append([
                $("<td>").html(data['word']),
                $("<td class=\"scoreValue\">").html(data['score']),
                $("<td>").html(data['humour']),
                $("<td>").html(data['ambiguity']),
                $("<td>").html(data['relatives'])
            ]);
            $(".showTable").show();
        }
        else if (data.hasOwnProperty("error")) {
            alert("Word not found in WordNet.");
        }

    }
    );
}

function getBaseTable() {
    $("#wordTable > tbody").empty();
    $.get(APIURI + "/words?sortMethod=scoreInverse", function(data){
        words = data["results"];
        words.forEach((word) => {
            row = $(".wordTableBody").append("<tr class=\"wordRow\"></tr>");
            row.append([
                $("<td>").html(word['word']),
                $("<td class=\"scoreValue\">").html(word['score'].toFixed(5)),
                $("<td>").html(word['humour'].toFixed(8)),
                $("<td>").html(word['ambiguity']),
                $("<td>").html(word['relatives'].toFixed(5))
            ]);
        });
    });
}

function showTable() {
    $(".showTable").hide();
    $(".searchBox").val("");
    getBaseTable();
}
