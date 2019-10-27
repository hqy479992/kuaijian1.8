//全局变量
/*
window.onload=function(){
	get_progress_rate()
	setInterval(function(){get_progress_rate()}, 5000)
}

function get_progress_rate(){
	var obj={
		'progress':'progress'
	}
	$.ajax({
		url:'progress',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			console.log(data)
			if (data=='error') {
				//do nothing
			}
			else{
				data=JSON.parse(data)
				var progreessrate=data['progress_rate']*100
				$('h5.my-3').html(data['task_name'])
				$('div.progress-bar').css('width',progreessrate+'%')
				$('div.progress-bar span').text(progreessrate+'%')
			}
		}
	})
}*/