//全局变量

//这里与后端传给算法的数据保持一致，使用js中的对象来对等于python的字典
var config={}
//视频文件夹列表,为了给用户提示
var video_list={} 
//本次合成名
var task_name=''

window.onload=function(){
	//显示多个输入框，可以考虑给输入框加入title
	for (var i = 0; i < getParams('chanelsum'); i++) {
		if (i==0) {
			//如果需要再处理
		}
		else{
			$('.chanelnum').children('div.input-group-append').before('<input type="text" class="form-control" value="">')
			$('.windowsize').children('div.input-group-append').before('<input type="text" class="form-control" value="">')
			$('.minoutputduration').children('div.input-group-append').before('<input type"text" class="form-control" value="">')
			$('.maxoutputduration').children('div.input-group-append').before('<input type="text" class="form-control" value="">')
			$('input').css('text-align','center')
		}
	}
	//先请求后台config默认值
	var obj={
		'chanelsum':getParams('chanelsum')
	}
	$.ajax({
		url:'/getDefaultConfig',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			if (data=='error') {
				//do nothing
			}
			else{
				data=JSON.parse(data)
				config=data['config']
				video_list=data['video_list']
				showconfig(config)
			}
		}
	})
}

//click事件
$('#startsyn').click(function(){
	task_name=$($('div.col-10 input')[0]).val()
	if (task_name=='') {
		//必须填写！
		$('#nameError').attr('class','alert alert-danger mt-1 py-1').attr('role','alert')
		$('#nameError').append('必须填写本次合成名字！')
	}
	else{
		config['head_duration']=Number($($('div.col-10 input')[1]).attr('value'))
		config['tail_duration']=Number($($('div.col-10 input')[2]).attr('value'))
		for (var i = 0; i < getParams('chanelsum'); i++) {
			config['window_size_'+i.toString()]=Number($('.windowsize').children('input').eq(i).attr('value'))
			config['min_output_duration_'+i.toString()]=Number($('.minoutputduration').children('input').eq(i).attr('value'))
			config['max_output_duration_'+i.toString()]=Number($('.maxoutputduration').children('input').eq(i).attr('value'))
		}
		var obj={
			'config':config,
			'task_name':task_name
		}
		$.ajax({
			url:'/settingsvalue',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if (data=='success') {
					window.location.href='/moredoing?task_name='+task_name;
				}
				else{
					//do nothing
				}
			}
		})
	}
})

//其他事件
function showconfig(config){
	$('.headduration').attr('value',config['head_duration'])
	$('.tailduration').attr('value',config['tail_duration'])
	for (var i = 0; i < getParams('chanelsum'); i++) {
		var videoname=video_list[i][0].substr('static/uploadfiles\\'.length)
		$('.chanelnum').children('input').eq(i).attr('value','通道'+(i+1).toString()).attr('disabled','true').css('border-bottom','0px').css('border-top','0px')
		$('.windowsize').children('input').eq(i).attr('value',config['window_size_'+i.toString()]).attr('title',videoname.slice(0,videoname.lastIndexOf('\\'))).attr('data-toggle','tooltip').attr('data-placement','bottom')
		$('.minoutputduration').children('input').eq(i).attr('value',config['min_output_duration_'+i.toString()]).attr('title',videoname.slice(0,videoname.lastIndexOf('\\'))).attr('data-toggle','tooltip').attr('data-placement','bottom')
		$('.maxoutputduration').children('input').eq(i).attr('value',config['max_output_duration_'+i.toString()]).attr('title',videoname.slice(0,videoname.lastIndexOf('\\'))).attr('data-toggle','tooltip').attr('data-placement','bottom')
	}
	$('[data-toggle="tooltip"]').tooltip()
}

$('input').css('text-align','center')