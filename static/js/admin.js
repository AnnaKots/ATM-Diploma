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

                    $('#total').find('span').text(Math.round(result[0] / 100) * 100);
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


});