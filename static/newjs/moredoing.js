//全局变量
var task_list = [];
var bari;

window.onload = function () {

	getProgress()
    setInterval(function () { moreTask() }, 5000)
}

function getProgress() {
	var obj = {
		'task_name': 'task_name',
		'progress_rate': 'progress_rate'
	}
	$.ajax({
		url: '/progress',
		type: 'POST',
		data: JSON.stringify(obj),
		async: true,
		success: function (data) {
			if (data == 'error') {
				//error
			} else {
				data = JSON.parse(data)
				moreTask(data)

			}
		}

	})
}

function moreTask(data){
    $.each(data, function (i, item) {
					console.log(item.task_name)
					console.log(item.progress_rate)
					$('.bar').append(`
                             	<div class="row bar-list">
                                    <div class="col-2">
                                        <span>${item.task_name}</span>
                                    </div>
                                    <div class="progress  col-9 mt-2 " style = "padding:0px;">
                                        <div class="progress-bar progress-bar-striped progress-bar-animated bg-info" id="bar${i}" role="progressbar" aria-valuemin="0" aria-valuemax="100" style=""><span></span></div>
                                    </div>
                                    <div class="col-1">
                                        <span class="fa fa-times-circle task"  onclick="closeBar(event,\'${item.task_name}\')"></span>
                                    </div>
			                    </div>`)

								var rate = item.progress_rate * 100
								rate = rate.toFixed(2)
								bari = 'bar'+i.toString()
								$('div#'+bari).css('width', rate + '%')
								$('div#'+bari+' span').text(rate + '%')

				})
}

//关闭
function closeBar(e, name) {
	// name = name || "";
	$(e.target).parent().parent().remove();
	// task_list.splice(task_list.indexOf(name), 1);
	var obj = {
		'task_name': name
	}
	$.ajax({
		url: '/stop_task',
		type: 'POST',
		data: JSON.stringify(obj),
		async: true,
		success: function (data) {
			if (data == 'error') {
				//    console.log("交互失败")
			}
			else {
				console.log(data)
			}
		}
	})
}

