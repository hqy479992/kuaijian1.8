'use strict'
//全局变量
var uploadfoldergroupnum=0

window.onload = function(){
}

//click事件
var adduploadfolder=function(){
	uploadfoldergroupnum+=1
	$('#uploadfoldergroup').append(
		$('<div>').attr('class','input-group pt-3').append(
			$('<div>').attr('class','input-group-prepend').append(
				$('<button>').attr('class','input-group-text fa fa-folder-open').attr('disabled','true')),
			$('<div>').attr('class','custom-file').append(
				$('<input>').attr('type','file').attr('class','custom-file-input').attr('id','inputfolder'+uploadfoldergroupnum.toString()).attr('webkitdirectory','true').attr('onchange','fileschosed(this.files,this)'),
				$('<label>').attr('class','custom-file-label').attr('for','inputfolder'+uploadfoldergroupnum.toString()).attr('id','inputfolderlabel'+uploadfoldergroupnum.toString()).append('选择文件夹...')),
			$('<div>').attr('class','input-group-append').append(
				$('<button>').attr('onclick','adduploadfolder()').attr('class','btn btn-outline-secondary').attr('type','button').attr('data-toggle','tooltip').attr('data-placement','bottom').attr('title','添加上传框').append(
					$('<span>').attr('class','fa fa-plus')))),
		$('<div>').attr('id','uploadfolderappendprogress'+uploadfoldergroupnum.toString()))
}

//change事件
var fileschosed=function(value,thisinput){
	$(thisinput).next().html('共有'+value.length.toString()+'个文件')
	var fd = new FormData()
	for (var i = 0; i < value.length; i++) {
		fd.append('file',value[i])
		fd.append('path',value[i]['webkitRelativePath'])
	}
	$.ajax({
		url:'/uploadfile',
		type:'POST',
		data:fd,
		contentType:false,
		processData:false,
		cache:false,
		xhr:function(){
			if ($(thisinput).parent().parent().next().html()=='') {
				$(thisinput).parent().parent().next().append(
					$('<div>').attr('class','progress mt-1').append(
						$('<div>').attr('class','progress-bar progress-bar-striped bg-info progress-bar-animated')
								.attr('role','progressbar').attr('aria-valuemin','0').attr('aria-valuemax','100')))
			}
			var myxhr=$.ajaxSettings.xhr()
			if (myxhr.upload) {
				myxhr.upload.addEventListener('progress',function(e){
					if(e.lengthComputable){
						var percent= Math.floor(e.loaded/e.total*100)
						$(thisinput).parent().parent().next().children('div').children('div').css('width',percent.toString()+'%')
						$(thisinput).parent().parent().next().children('div').children('div').html(percent.toString()+'%')
					}
				},false)
			}
			return myxhr
		},
		success: function(data){
			if (data=='success'&&$(thisinput).parent().parent().next().children('div').children('div').html()=='100%') {
				setTimeout(function() {$(thisinput).parent().parent().next().html('')}, 2000)
			}
		}
	})
}