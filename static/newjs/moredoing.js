var task_list = [];
$(function () {
	getProgress();
	createList(task_list)
	createBar(task_list)
	setInterval(function () { moreTask() },5000)
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

				if (task_list.length==0) {
					$('.col-10').append(`
							<h4 class="text-center text-black-50 mt-5 pt-5">
								<span class="fa fa-hourglass-o mr-3"></span>
								没有正在合成的任务...
							</h4>
						`)
				}
				else{
					$('.col-10').html('');
					return task_list;
				}

			}
		}
	})
}

//动态创建列表
function createList(data) {
	$.each(data, function (index, item) {
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
	$.each(data, function (index, item) {
	    var rate = item.progress_rate *100
	    rate  = rate.toFixed(2);
		$(".bar-list" + index).append(`
		<br>
		<div class="progress col-10 mt-2 ml-3 row" style="padding:0">
		<div class="progress-bar progress-bar-striped progress-bar-animated bg-info"  role="progressbar" aria-valuemin="0" aria-valuemax="100"  style="width:${rate == 0 ?0:rate}%">
		    <span style="color:black">${rate == 0 ? '正在等待' : rate+"%"}</span>
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
					if ($('.bar-list'+index).find('.progress-bar').children('span').html()=="2.00%") {
						window.location.reload()
						$('.bar-list'+index).remove()

					}else{
                        $(".bar-list" + index + " .progress-bar").css("width",rate == 0 ? "0.00%":rate + "%");
                        $(".bar-list" + index + " .progress-bar").html(`<span style="color:black">${rate == 0 ? '正在等待' : rate+"%"}</span>`);
					}

				})
			}
		}

	})
}
function closeBar(e, name) {
	// name = name || "";
	$(e.target).parent().parent().remove();
	 task_list.splice(task_list.indexOf(name), 1);
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
				console.log("交互失败")
			}
			else {
				console.log(data)
				window.location.reload();
			}
		}
	})
}``