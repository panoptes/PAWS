var ws;
function WebSocketTest(server) {
    var ws;
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://" + server + "/ws/");
        ws.onopen = function() {
            ws.send('get_status');
        };
        ws.onmessage = function (evt) {
            var type = evt.data.split(' ', 1)[0];
            var received_msg = evt.data.substring(evt.data.indexOf(' ') + 1)

            var msg = jQuery.parseJSON(received_msg);

            switch(type.toUpperCase()){
                case 'STATE':
                    change_state(msg['state']);
                    break;
                case 'STATUS':
                    change_state(msg['state']);
                    update_info(msg['observatory']);
                    refresh_images();
                    break;
                case 'ENVIRONMENT':
                    update_environment(msg['data']);
                    break;
                case 'WEATHER':
                    update_info(msg['data']);
                    update_weather(msg['data']);
                    break;
                case 'CAMERA':
                    update_cameras(msg);
                    break;
                case 'SAYBOT':
                case 'PANSHELL':
                    add_chat_item(type, msg.message, msg.timestamp);
                    break;
                default:
                    break;
            }

        };
        ws.onclose = function() {
            toggle_status('off');
        };
    } else {
        toggle_status('error');
    }

    return ws;
}

function add_chat_item(name, msg, time){

    item = '<div class="callout padded light-gray">';
    item = item + ' <img src="/static/img/pan.png" alt="user image" class="avatar">';
    item = item + ' <small class="float-right"><i class="fa fa-clock-o"></i> ' + time +' UTC</small>';
    item = item + '  <p class="message">';
    item = item + '    <a href="#" class="name">';
    item = item + name;
    item = item + '    </a>';
    item = item + msg;
    item = item + '  </p>';
    item = item + '</div>';

    $('#bot_chat').prepend(item);
}

function toggle_connection_icon(icon){
    console.log('Should toggle status here');
    // $(icon).toggleClass('success').toggleClass('danger');
    // $(icon).toggleClass('fa-check-circle-o').toggleClass('fa-exclamation-triangle');
}

function update_environment(info){
    var computer_info = info['computer_box'];
    var camera_info = info['camera_box'];

    $('.computer_box_humidity_00').html(computer_info['humidity']);
    $('.camera_box_humidity_00').html(camera_info['humidity']);

    $('.camera_box_temp_00').html(camera_info['temp_00']);
    $('.computer_box_temp_00').html(computer_info['temp_00']);
    $('.computer_box_temp_01').html(computer_info['temp_01']);
    $('.computer_box_temp_02').html(computer_info['temp_02']);
    $('.computer_box_temp_03').html(computer_info['temp_03']);
}

function update_weather(is_safe){
    if(is_safe){
        $('.safe_condition').html('Safe').addClass('success');
        $('.title-bar').removeClass('danger');
        $('.callout').removeClass('unsafe_borders').addClass('safe_borders');
    } else {
        $('.safe_condition').html('Unsafe');
        $('.title-bar').addClass('danger');
        $('.callout').addClass('unsafe_borders').removeClass('safe_borders');
    }
}

function toggle_status(status){
    var icon = $('.current_state i');
    var text = $('.current_state span');

    icon.removeClass().addClass('fa');
    if (status == 'on'){
        icon.addClass('fa-circle').addClass('success');
        text.html('Online');
    } else if (status == 'off'){
        icon.addClass('fa-bolt').addClass('danger');
        text.html('Offline').addClass('danger');
    } else {
        icon.addClass('fa-exclamation-triangle', 'danger').addClass('danger');
        text.html('Error').addClass('danger');
    }
}

function change_state(state){
    var icon = $('.current_state i');
    var text = $('.current_state span');

    icon.removeClass().addClass('fa').addClass('success');
    text.html(state.toUpperCase());
    switch(state) {
        case 'analyzing':
            icon.addClass('fa-calculator');
            break;
        case 'tracking':
            icon.addClass('fa-binoculars');
            break;
        case 'observing':
            icon.addClass('fa-camera');
            break;
        case 'pointing':
            icon.addClass('fa-bullseye');
            break;
        case 'slewing':
            icon.addClass('fa-cog fa-spin');
            break;
        case 'scheduling':
            icon.addClass('fa-tasks');
            break;
        case 'ready':
            icon.addClass('fa-thumbs-o-up');
            break;
        case 'parking':
        case 'parked':
            icon.addClass('fa-car');
            break;
        case 'sleeping':
            icon.addClass('fa-check-circle');
            break;
        default:
            icon.addClass('fa-circle');
    }
    reload_img($('.state_img img'));
}

// Find all the elements with the class that matches a return value
// and update their html
function update_info(status){
    $.each(status, function(key, val){
        $('.' + key).each(function(idx, elem){
            $(elem).html(val);
        })
    });
}

function update_cameras(cameras){
    $.each(cameras, function(cam_name, props){
        $.each(props, function(prop, val){
            $('#' + cam_name + ' .' + prop).each(function(idx, elem){
                $(elem).html(val);
            });
            if (prop == 'exptime'){
                // Start the progress bar
                var pb = $('#' + cam_name + ' .progress-bar');
                pb.width('100%');

                var exptime = $('#' + cam_name + ' .exptime');
                exptime.html(val);

                var total_time = val;
                var count_time = val;

                var exp_count = $('#' + cam_name + ' .exp_count');
                // exp_count.timer('remove');
                exp_count.timer({
                    duration: '2s',
                    callback: function(){
                        count_time = count_time - 2;
                        var perc = (count_time/total_time) * 100;
                        console.log(perc);

                        if (perc < 0){
                            pb.width('0%');
                            exp_count.timer('remove');
                        } else {
                            pb.width(perc + '%');
                        }

                    },
                    repeat: true,
                });


                var pb_count = function(cb, count){
                    var width_perc = (count / val) * 100;
                    pb.width(width_perc + '%');
                    setTimeout(cb, 1000, cb, --count);
                };

                setTimeout(pb_count, 1000, pb_count, val);
            }
        });

    });

}

// Refresh all images with `img_refresh` container class
function refresh_images(){
    $.each($('.img_refresh img'), function(idx, img){
        reload_img(img);
    });
}

// Reload individual image
function reload_img(img){
    base = $(img).attr('src').split('?')[0];
    // console.log("Reloading image: " + $(img).attr('src'));

    // Hack for others
    if(base.startsWith('http')){
        new_src = $(img).attr('src');
    } else {
        new_src = base + '?' + Math.random()
    }

    $(img).attr('src', new_src);
}
