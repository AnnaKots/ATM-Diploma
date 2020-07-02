$(document).ready(function () {

    $(function () {
        $("#date").datepicker();
    });


    $('#calculation').click(function () {
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        var atm_name = $('#atm_name').val();
        var date = $('#date').val();
        var festival = $('#festival').val();
        var working_day = $('#working_day').val();

        if (date == '') {
            alert('Введите дату для рассчета');
            return;
        }

        $('#calculation').css('display', 'none');
        $('#calculation').after('<p class="loading" style="font-size: 20px; font-weight: bold;">Загрузка результатов....</p>');
        if (atm_name) {
            $.ajax({
                type: "POST",
                url: "../../calculate/",
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'atm_name': atm_name,
                    'date': date,
                    'festival': festival,
                    'working_day': working_day
                },
                cache: false,
                success: function (data) {
                    var result = data.split('\n');

                    $('#total_head');
                    $('#total').find('span').text(Math.round(result[0] / 100) * 100);

                    $('#total_head').css('display', 'block');
                    $('#total').css('display', 'block');
                    $('.loading').css('display', 'none');
                    $('.res_data').css('display', 'block');
                    $('#calculation').css('display', 'initial');

                }, error: function (jqXHR, status, e) {
                    if (status === "timeout") {
                        alert("Время ожидания ответа истекло!");
                    } else {
                        alert(status);
                    }
                }
            });
        }
    });

    $('#calculation_for_all').click(function () {
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        var date = $('#date').val();
        var festival = $('#festival').val();
        var working_day = $('#working_day').val();

        if (date == '') {
            alert('Введите дату для рассчета');
            return;
        }

        $('#calculation_for_all').css('display', 'none');
        $('#calculation_for_all').after('<p class="loading" style="font-size: 20px; font-weight: bold;">Загрузка результатов....</p>');
        if (date) {
            $.ajax({
                type: "POST",
                url: "../../for_all_calculate/",
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'date': date,
                    'festival': festival,
                    'working_day': working_day
                },
                cache: false,
                success: function (data) {
                    var result = data.split('\n');

                    let names = ['Главная_улица', 'Парк', 'Аэропорт', 'Центр', 'Университет'];

                    $('#total_head');
                    $('#total').find('span').text(names[0] + ': ' + Math.round(result[0] / 100) * 100);
                    $('#total1').find('span').text(names[1] + ': ' + Math.round(result[1] / 100) * 100);
                    $('#total2').find('span').text(names[2] + ': ' + Math.round(result[2] / 100) * 100);
                    $('#total3').find('span').text(names[3] + ': ' + Math.round(result[3] / 100) * 100);
                    $('#total4').find('span').text(names[4] + ': ' + Math.round(result[4] / 100) * 100);

                    $('#total_head').css('display', 'block');
                    $('#total').css('display', 'block');
                    $('#total1').css('display', 'block');
                    $('#total2').css('display', 'block');
                    $('#total3').css('display', 'block');
                    $('#total4').css('display', 'block');
                    $('.loading').css('display', 'none');
                    $('.res_data').css('display', 'block');
                    $('#calculation_for_all').css('display', 'initial');

                }, error: function (jqXHR, status, e) {
                    if (status === "timeout") {
                        alert("Время ожидания ответа истекло!");
                    } else {
                        alert(status);
                    }
                }
            });
        }
    });


});