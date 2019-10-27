//全局变量
var task_list = [];

window.onload = function () {
    var obj={
        'getAllTasks':'ger_all_task'
    }
    $.ajax({
        url:'/get_all_task',
        type:'POST',
        data:JSON.stringify(obj),
        async:true,
        success:function(data){
            if(data=='error'){
                //error
            }
            else{
                task_list=JSON.parse(data)
                moreTask(task_list);
	            setInterval(function () { barMoreTask(task_list) }, 5000)
            }
        }
    })

}
function getProgress(obj){
	$.ajax({
		url: '/progress',
		type: 'POST',
		data: JSON.stringify(obj),
		async: true,
		success: function (data) {
			if (data == 'error') {
				//do nothing
			}
			else {
				data = JSON.parse(data)
				var progreessrate = data['progress_rate'] * 100
				$('div.progress-bar').css('width', progreessrate + '%')
				$('div.progress-bar span').text(progreessrate + '%')
			}
		}
	})
}
function barMoreTask(list) {
	for (var item of list) {
		var obj = {
			'progress': 'progress',
			'task_name': item
		}
		getProgress(obj);
	}
}


//多进程
function moreTask(task_list) {
	for (var item of task_list) {
		$('.bar').append(`
	   <div class="row bar-list">
			<div class="col-2">
				<span>${item}</span>
			</div>
			<div class="progress  col-9 mt-2 " style = "padding:0px;">
				<div class="progress-bar progress-bar-striped progress-bar-animated bg-info" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="">
					<span>${item}</span>
				</div>
			</div>
			<div class="col-1">
				<span class="fa fa-times-circle task"  onclick="closeBar(event,${item})"></span>
			</div>
		   </div>`)
		var obj = {
			'progress': 'progress',
			'task_name': item
		}
		getProgress(obj);
	}
}

//关闭
function closeBar(e, name) {
	// console.log($(e.target).parent().parent());//隐藏
	// console.log(task_list,name)
	console.log(name)
	$(e.target).parent().parent().remove();
	name = name.toString();
	console.log(name)
	task_list.splice(task_list.indexOf(name), 1);
	var obj={
	    'task_name':name
	}
	$.ajax({
	    url:'/stop_task',
	    type:'POST',
	    data:JSON.stringify(obj),
	    async:true,
	    success:function(data){
            if(data=='error'){

            }
            else{
                console.log(data)
            }
	    }
	})
	console.log(task_list)
}

