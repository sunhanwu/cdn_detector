<template>
    <div>
        <el-row>
        <el-card>
        <!-- <div id="toolbar">
            <div class="ibox-title">
                <h5>查询结果</h5>
            </div>
        </div> -->
            
        <el-input v-model="input" placeholder="请输入CDN域名" style="display:inline-table; width: 10%; float:left" @input.native="btn()" ></el-input>
          <table
            id="CDN"
            data-height="800"
            class="table table-bordered table-striped"
            data-classes="table table-hover table-condensed"
            data-mobile-responsive="true"
            data-toolbar="#toolbar"
            data-show-toggle="true"
            data-show-columns="true"
            data-show-export="true"
            data-minimum-count-columns="2"
            data-id-field="id"
            data-page-list="[10, 25, 50, 100, ALL]"
            data-show-footer="false"
            data-side-pagination="server"
            data-response-handler="responseHandler"
            data-click-to-select="true">
            <thead>
                <tr>
                <th data-field="rawdomain">原始域名</th>
                <th data-field="cdndomain">CDN域名</th>
                <th data-field="region">地区</th>
                <th data-field="ipaddress">IP</th>
                </tr>
            </thead>
          </table>
            <!--data-url="/dns-serve/api/domainExhibition/blacklist/whitelisttop10"/>-->       
        </el-card>
        </el-row>
     </div>   
</template>

<script>
import $ from 'jquery'
export default {
    name:'finall',
    data(){
        return{
          bookList:[],
          bookList1:[], 
          search:'',
          input:'',
          columnsWhite: [
          {
            field: 'rawdomain', // 序号'
            // type:'index',
            title: '原始域名',
            align: 'center', // 对其方式
            valign: 'middle', // 对其方式
            // sortable: true
          },
          {
            field: 'cdndomain',
            title: 'CDN域名',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
          {
            field: 'region',
            title: '地区',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
          {
            field: 'ipaddress',
            title: 'IP',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
        ],
        }
    },
    mounted() {        
        // $('#CDN').bootstrapTable('destroy').bootstrapTable({
        //     showExport: true,
        //     exportDataType: 'all',
        //     exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel', 'doc'],
        //     columns: this.columnsWhite,
        //     // data: this.data,
        //     showToggle: true,
        //     responseHandler(res) {
        //     console.log('1234');
        //     return {
        //         "rows": res.rows,
        //         "total": res.total
        //     }
        //     },
        //     onLoadSuccess(res) {
        //     // console.log(res);
        //     },
        // });
        this.getlist();
  },
    methods: {
    export1(data){
      window.open(data,'_blank'); 
    },
    searchnews(){
    //   this.search=this.$route.query.search  
    //   this.$http.get('http://127.0.0.1:8000/api/add?search=' + this.search)
    //     .then((response) => {
    //       console.log('7',response)
    //       var res = JSON.parse(response.bodyText)
    //       this.bookList=res.msg
    //       console.log('1',this.bookList)
    //     })
        this.data = [{rawdomain:'1',cdndomain:'www.baidu.com',region:'China',ipaddress:'192.123.123.1'}]
        // $("#CDN").bootstrapTable('resetSearch', this.search);  
        $('#CDN').bootstrapTable("load", this.data)
    },
    getlist(){
        this.data = [{rawdomain:'1',cdndomain:'www.baidu.com',region:'China',ipaddress:'192.123.123.1'},{rawdomain:'2',cdndomain:'www.google.com',region:'America',ipaddress:'192.123.23.2'}]
        // $("#CDN").bootstrapTable('resetSearch', this.search);  
        // $('#CDN').bootstrapTable("load", this.data)
        $('#CDN').bootstrapTable({
            data: this.data
            })
        console.log(this.data)
    },
    btn:function(){
      console.log(this.input)        
      var search = this.input;
      if (search) {
        this.searchData = this.data.filter(function(product) {
          // console.log('1',product)
          return Object.keys(product).some(function(key) {
            // console.log('2',key)
            return String(product['cdndomain']).toLowerCase().indexOf(search) > -1
          })
        })
        $('#CDN').bootstrapTable("load", this.searchData)  
      }
      else{
        $('#CDN').bootstrapTable("load", this.data)  
      }          
      }
  }
}
</script>

<style scoped lang="scss">
  .ibox-title {
    background-color: #fff;
    border-color: #e7eaec;
    color: inherit;

    h5 {
      display: inline-block;
      font-size: 16px;
      margin: 0 0 7px;
      padding: 0;
      text-overflow: ellipsis;
      font-weight: 700;
      color: #007bff;
    }
  }
</style>