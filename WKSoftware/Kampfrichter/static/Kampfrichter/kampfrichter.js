//console logs in nachricht für user ändern!
function myCode() {
var isOnline = window.navigator.onLine;
if (isOnline){
    document.getElementById("internet_info").style.display = "none";
}
else{
    document.getElementById("internet_info").style.display = "initial";
}};

var tid = setInterval(myCode,2000);

$(document).ready(function(){

    function is_relay(){
        selected_run = $('#id_lauf').val(); //name of selected run in sel#ect field
        return relays.includes(selected_run);
    };

    function relay_correction_fields(){
        if (is_relay()){
            $('#id_wechsel_bereit').show();
            $("label[for='id_wechsel_bereit']").show();
        }
        else{
            $('#id_wechsel_bereit').hide();
            $("label[for='id_wechsel_bereit']").hide();
        };
    };

    function handoff_is_ready(){
        selected_name = $('#id_lauf').val();
        selected_sex = $('#id_geschlecht').val();
        selected_age = $('#id_alter').val();
        selected_number = parseInt($('#id_laufnummer').val());
        string_selected = selected_name + selected_sex + selected_age + selected_number;
        is_ready = relays_data[string_selected];
        if (is_ready){
            return is_ready;
        };
    };

    function relay_correction_values(){
        if (handoff_is_ready()){
        //check if handoff field is true
            $('#id_wechsel_bereit').prop( "checked", true );
        }
        else{
            $('#id_wechsel_bereit').prop( "checked", false );
        };
    };

    function is_violation(){
        selected_name = $('#id_lauf').val();
        selected_sex = $('#id_geschlecht').val();
        selected_age = $('#id_alter').val();
        selected_number = $('#id_laufnummer').val();
        string_selected = selected_name + selected_sex + selected_age + selected_number;
        bool_violation = runs_data[string_selected];
        if (bool_violation){
            return bool_violation;
        };
    };

    function run_correction_values(){
        if (is_violation()){
        $('#id_verstoß_existent').prop( "checked", true );
        }
        else{
        $('#id_verstoß_existent').prop( "checked", false );
        };
    };

    function is_run(){
        selected_name = $('#id_lauf').val();
        selected_sex = $('#id_geschlecht').val();
        selected_age = $('#id_alter').val();
        selected_number = $('#id_laufnummer').val();
        string_selected = selected_name + selected_sex + selected_age + selected_number;
        bool_check = runs_data[string_selected];
        if (bool_check == undefined){
            $('#id_info').show();
        }
        else{
            $('#id_info').hide();
        };
    };

    function data_change(){
        run_correction_values();
        relay_correction_fields();
        if (is_relay()){
        //run is relay --> show handoff field
            relay_correction_values();
        };
        is_run();
    };

    //changes for the default run selection:
    relay_correction_fields();
    relay_correction_values();

    run_correction_values();
    is_run();

    $("#id_lauf").change(function(){
        data_change();
    });
    $("#id_geschlecht").change(function(){
        data_change();
    });
    $("#id_alter").change(function(){
        data_change();
    });
    $("#id_laufnummer").change(function(){
        data_change();
    });
    //classes in django forms are too inconvenient ATM, i think the solution would be:
    //https://docs.djangoproject.com/en/2.1/topics/forms/#rendering-fields-manually
});
