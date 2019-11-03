var task_list = [];
$(function () {
	getProgress();
	createList(task_list)
	createBar(task_list)
	setInterval(function () { moreTask() },2000)
})
//请求到数据
function getProgress() {
	var obj = {
		'task_name': 'task_name',
		'progress_rate': 'progress_rate'
	}
	$.ajax({
		url: '/progress',
		type: 'POST',
		data: JSON.stringify(obj),
		async: false,
		success: function (data) {
			if (data == 'error') {
				//error
			} else {
				task_list = JSON.parse(data)
			}
		}

	})
	return task_list;
}

//动态创建列表
function createList(data) {
	$.each(data, function (index, item) {
		$(".bar").append(`
				<div class="row bar-list bar-list${index}">
					<div class="col-2">
						<span>${item.task_name}</span>
					</div>
					<div class="col-1">
						<span class="fa fa-times-circle task"  onclick="closeBar(event,\'${item.task_name}\')"></span>
					</div>
				</div>
			`)
	})
}
// 进度条列表
function createBar(data) {
	$.each(data, function (index, item) {
	    var rate = item.progress_rate *100
	    rate  = rate.toFixed(3);
		$(".bar-list" + index).append(`
		<div class="progress  col-9 mt-2 " style = "padding:0px;">
		<div class="progress-bar progress-bar-striped progress-bar-animated bg-info"  role="progressbar" aria-valuemin="0" aria-valuemax="100"  style="width: ${rate}%;">
		    <span>${rate}%</span>
		</div>
	</div>
		`)
	})
}
function moreTask(){
	var obj = {
		'task_name': 'task_name',
		'progress_rate': 'progress_rate'
	}
	$.ajax({
		url: '/progress',
		type: 'POST',
		data: JSON.stringify(obj),
		async: false,
		success: function (data) {
			if (data == 'error') {
				//error
			} else {
				$.each(JSON.parse(data),function(index,item){
				   var rate = item.progress_rate *100
	                rate  = rate.toFixed(3);
					$(".bar-list" + index + " .progress-bar").css("width",rate+"%");
					$(".bar-list" + index + " .progress-bar span").text(rate+"%");
				})
			}
		}

	})
}
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