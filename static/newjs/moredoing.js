var task_list = [{"task_name":"test1","progress_rate":"1.0000"},{"task_name":"test2","progress_rate":0.8923}];
console.log(task_list)
$(function () {
	//getProgress();
	createList(task_list)
	createBar(task_list)
	//setInterval(function () { moreTask() },5000)
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
				if (task_list==[]) {
					$('.col-10').append(`

						`)
				}
			}
		}
	})
}

//动态创建列表
function createList(data) {
	$.each(task_list, function (index, item) {
		$(".bar").append(`
				<div class="row bar-list bar-list${index} pt-3">
					<div class="col-9">
						<h3>${item.task_name}</h3>
					</div>
					<div class="col-3">
						<button class="btn btn-secondary"  onclick="closeBar(event,\'${item.task_name}\')">
						    <span class="fa fa-times"></span>取消合成
						</button>
					</div>
				</div>
			`)
	})
}
// 进度条列表
function createBar(data) {
	$.each(task_list, function (index, item) {
	    var rate = item.progress_rate *100
	    rate  = rate.toFixed(2);
		$(".bar-list" + index).append(`
		<br>
		<div class="progress col-10 mt-2 ml-3 row" style="padding:0">
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
	                rate  = rate.toFixed(2);
					$(".bar-list" + index + " .progress-bar").css("width",rate+"%");
					$(".bar-list" + index + " .progress-bar span").text(rate+"%");
					if ($('.bar-list'+index).find('.progress-bar').children('span').html()=="100.00%") {
						$('.bar-list'+index).remove()
					}
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