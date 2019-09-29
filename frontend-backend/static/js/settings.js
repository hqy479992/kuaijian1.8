//全局变量

//这里与后端传给算法的数据保持一致，使用js中的对象来对等于python的字典
var config={}
//本次合成名
var task_name=''

window.onload=function(){
	//显示多个输入框，可以考虑给输入框加入title
	for (var i = 0; i < getParams('chanelsum'); i++) {
		if (i==0) {
			$('.windowsize').children('div.input-group-append').prev().attr('title','')
			$('.minoutputduration').children('div.input-group-append').prev()
			$('.maxoutputduration').children('div.input-group-append').prev()
		}
		else{
			$('.windowsize').children('div.input-group-append').before('<input type="text" class="form-control" value="">')
			$('.minoutputduration').children('div.input-group-append').before('<input type"text" class="form-control" value="">')
			$('.maxoutputduration').children('div.input-group-append').before('<input type="text" class="form-control" value="">')
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
				config=JSON.parse(data)
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
		$($('div.col-10 input')[0]).attr('placeholder','ERROR!必须填写！')
	}
	config['head_duration']=$($('div.col-10 input')[1]).val()
	config['tail_duration']=$($('div.col-10 input')[2]).val()
	for (var i = 0; i < getParams('chanelsum'); i++) {
		config['window_size_'+i.toString()]=$('.windowsize').children('input').eq(i).attr('value')
		config['min_output_duration_'+i.toString()]=$('.minoutputduration').children('input').eq(i).attr('value')
		config['max_output_duration_'+i.toString()]=$('.maxoutputduration').children('input').eq(i).attr('value')
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
				window.location.href='/doing'
			}
			else{
				//do nothing
				console.log('error')
			}
		}
	})
})

//其他事件
function showconfig(config){
	$('.headduration').attr('value',config['head_duration'])
	$('.tailduration').attr('value',config['tail_duration'])
	for (var i = 0; i < getParams('chanelsum'); i++) {
		if (i==0) {
			$('.windowsize').children('input').eq(0).attr('value',config['window_size_0'])
			$('.minoutputduration').children('input').eq(0).attr('value',config['min_output_duration_0'])
			$('.maxoutputduration').children('input').eq(0).attr('value',config['max_output_duration_0'])
		}
		else{
			$('.windowsize').children('input').eq(i).attr('value',config['window_size_'+i.toString()])
			$('.minoutputduration').children('input').eq(i).attr('value',config['min_output_duration_'+i.toString()])
			$('.maxoutputduration').children('input').eq(i).attr('value',config['max_output_duration_'+i.toString()])
		}
	}
	$('[data-toggle="tooltip"]').tooltip()
}