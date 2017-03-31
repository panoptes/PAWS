var ws;

var exp_num = 0;

function WebSocketTest(server) {
    var ws;
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://" + server + "/ws/");
        ws.onopen = function() {
            toggle_status('on');
            console.log("Connection established");
        };
        ws.onmessage = function (evt) {
            var channel = evt.data.split(' ', 1)[0];
            var received_msg = evt.data.substring(evt.data.indexOf(' ') + 1)

            var msg = jQuery.parseJSON(received_msg);

            switch(channel.toUpperCase()){
                case 'STATE':
                    change_state(msg['state']);
                    break;
                case 'OBSERVER':
                    update_info(msg['observer']);
                    break;
                case 'FIELD':
                    update_info(msg['field']);
                    break;
                case 'STATUS':
                    change_state(msg['state']);

                    var observer = msg['observatory']['observer'];
                    var observation = msg['observatory']['observation'];

                    observer['local_evening_astro_time'] = trim_time(observer['local_evening_astro_time']);
                    observer['local_morning_astro_time'] = trim_time(observer['local_morning_astro_time']);

                    observer['local_moon_illumination'] = pretty_number(observer['local_moon_illumination'] * 100);
                    observer['local_moon_alt'] = pretty_number(observer['local_moon_alt']);

                    // Update parts of the page

                    if (observation){
                        update_info(observation);
                        if (observation['current_exp'] != exp_num){
                            // $('#observation_info .timer').timer('reset');
                            exp_num = observation['current_exp'];
                        }
                    }
                   
                    update_info(observer);
                    // $('#system_panel .timer').timer('reset');

                    update_info(msg['observatory']['mount']);
                    // $('#mount_panel .timer').timer('reset');

                    refresh_images();
                    break;
                case 'ENVIRONMENT':
                    update_environment(msg['data']);
                    break;
                case 'WEATHER':
                    update_info(msg['data']);
                    update_safety(msg['data']['safe']);

                    // $('#weather_panel .timer').timer('reset');
                    break;
                case 'CAMERA':
                    update_cameras(msg);
                    break;
                case 'PANBOT':
                case 'PANCHAT':
                case 'PEAS_SHELL':
                case 'POCS_SHELL':
                    add_chat_item(channel, msg.message, msg.timestamp);
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

function update_safety(is_safe){
    if(is_safe){
        $('.safe_condition').html('Safe').removeClass('text-danger').addClass('text-success');
        toggle_status('on');
    } else {
        $('.safe_condition').html('Unsafe').removeClass('text-success').addClass('text-danger');
        toggle_status('unsafe');
    }
}

function toggle_status(status){
    var safety_cls, border_cls;

    // Update depending on status
    if (status == 'on'){
        safety_cls = 'success';
        border_cls = 'safe_borders';
    } else if (status == 'off'){
        safety_cls = 'warning';
        border_cls = 'warning_borders';
    } else {
        safety_cls = 'danger';
        border_cls = 'unsafe_borders';
    }

    $('.safety-border').removeClass('safe_borders warning_borders unsafe_borders').addClass(border_cls);
}

/******************** Update Info Methods ****************************/

function change_state(state){
    var icon = $('.current_state i');
    var text = $('.current_state span');

    icon.removeClass().addClass('fa').addClass('success');
    text.removeClass('warning danger').html(state.toUpperCase());
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
    reload_img($('.state_img'));
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

function update_environment(info){
    try {
        if (info['name'] == 'camera_board'){
            var camera_info = info;
            $('.camera_box_humidity_00').html(pretty_number(camera_info['humidity']));
            $('.camera_box_temp_00').html(pretty_number(camera_info['temp_00']));
            $('.position_x').html(pretty_number(camera_info['accelerometer']['x']));
            $('.position_y').html(pretty_number(camera_info['accelerometer']['y']));
            $('.position_z').html(pretty_number(camera_info['accelerometer']['z']));
            $('.position_o').html(pretty_number(camera_info['accelerometer']['o']));
        }
    } catch(err) {
        console.log(err);
    }

    try {
        if (info['name'] == 'telemetry_board'){
            var computer_info = info;
            $('.computer_box_humidity_00').html(pretty_number(computer_info['humidity']));
            $('.computer_box_temp_00').html(pretty_number(computer_info['temp_00']));
            for (i = 0; i < computer_info['temperature'].length; i++){
                $('.computer_box_temp_0' + (i + 1)).html(pretty_number(computer_info['temperature'][i]));
            }
            $('.current_fan').html(computer_info['current']['fan']);
            $('.current_mount').html(computer_info['current']['mount']);
            $('.current_main').html(computer_info['current']['main']);
            $('.current_cameras').html(computer_info['current']['cameras']);

            if(computer_info['power']['fan'] == 1){
                $('.current_fan').prev().removeClass('danger');
            } else {
                $('.current_fan').prev().addClass('danger');
            }
            if(computer_info['power']['cameras'] == 1){
                $('.current_cameras').prev().removeClass('danger');
            } else {
                $('.current_cameras').prev().addClass('danger');
            }
            if(computer_info['power']['computer'] == 1){
                $('.current_computers').prev().removeClass('danger');
            } else {
                $('.current_computers').prev().addClass('danger');
            }
            if(computer_info['power']['mount'] == 1){
                $('.current_mount').prev().removeClass('danger');
            } else {
                $('.current_mount').prev().addClass('danger');
            }            
            if(computer_info['power']['weather'] == 1){
                $('.current_weather').prev().removeClass('danger');
            } else {
                $('.current_weather').prev().addClass('danger');
            }                        
        }
    } catch(err) {
        console.log(err);
    }
}

function add_chat_item(name, msg, time){

    item = '<div class="media">';
    item = item + '<div class="media-left">';
    item = item + ' <img src="/static/img/pan.png" alt="Bot Image" class="media-object avatar">';
    item = item + '</div>';
    item = item + '<div class="media-body">';
    item = item + ' <small class="float-right"><i class="fa fa-clock-o"></i> ' + time +' UTC</small>';
    item = item + ' <br /><span class="message">';
    item = item + '    <a href="#" class="name">';
    item = item + name;
    item = item + '    </a>';
    item = item + msg;
    item = item + '  </span>';
    item = item + '</div>';

    $('#bot_chat').prepend(item);
}

/******************** Convenience Methods ****************************/

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
        new_src = base + '?' + new Date().getTime();
    }

    $(img).attr('src', new_src);

    // Update the link so not pointing at thumbnail
    // $(img.parentlEement).attr('href', new_src.replace('tn_', ''));
}

function trim_time(t){
    var time = t;
    if (typeof(t) == 'string'){
        time = t.split(':').slice(0,-1).join(':');
    }
    return time;
}

function pretty_number(num){
    return parseFloat(num).toFixed(2);
}
