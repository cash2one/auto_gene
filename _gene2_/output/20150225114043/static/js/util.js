function check_all (v) {
    // 用于全选， 全不选
    if ($(v).prop('checked')) {
        $("table input[type=checkbox][name='record_id']").prop('checked',true);
     } else {
        $("table input[type=checkbox][name='record_id']").prop('checked',false);
     }
}
   
function operate_multiple (url, msg1, msg2) {
    // 用于勾选多个进行操作
    var tmp = $("input[type='checkbox'][name='record_id']:checked");
    if (tmp.length == 0) {
        alert ('请先选中数据');
        return false;
    }
    if (confirm (msg1+tmp.length+msg2)) {
        var xids = "";
        for (var i=0; i<tmp.length; i++) {
            xids += tmp[i].value+',';
        }
        var req = {'xids': xids};
        $.post(url, data=req, function (data) {
           alert (data.msg);
           location.reload(); 
        }, 'json');
    }
}