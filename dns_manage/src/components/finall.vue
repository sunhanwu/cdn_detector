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
                <th data-field="domain_name" >原始域名</th>
                <th data-field="ip_addr">CDN_IP</th>
                <th data-field="depth">深度</th>
                <th data-field="recur_server">地区</th>
                </tr>
            </thead>
          </table>
            <!--data-url="/dns-serve/api/domainExhibition/blacklist/whitelisttop10"/>-->       
        </el-card>
        </el-row>
        <el-row>    
          <div class="mynetwork" id="mynetwork"></div>
        </el-row>  
     </div>   
</template>

<script>
import $ from 'jquery'
import vis from 'vis'
export default {
    name:'finall',
    data(){
        return{
          bookList:[],
          vislist:[], 
          search:'',
          input:'',
          columnsWhite: [
          {
            field: 'domain_name', // 序号'
            // type:'index',
            title: '原始域名',
            align: 'center', // 对其方式
            valign: 'middle', // 对其方式
            // sortable: true
          },
          {
            field: 'ip_addr',
            title: 'CDN_IP',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
          {
            field: 'depth',
            title: '深度',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
          {
            field: 'recur_server',
            title: '递归服务器IP',
            valign: 'middle',
            halign: 'center',
            align: 'center',
            // sortable: true
          },
        ],
        nodes : [],
        edges : [],
              options: {},
        }
    },
    mounted() { 
        this.getlist();
  },
    methods: {
    export1(data){
      window.open(data,'_blank'); 
    },
    getlist(){
        this.search=this.$route.query.search
        this.$http.get('http://127.0.0.1:8000/query/?domain=' + this.search)
        .then((response) => {
          console.log('7',response)
          var res = JSON.parse(response.bodyText)
          console.log('7',res)
          this.bookList=res.mysql_lists[0]
          // this.vislist =res.neo4j_lists          
          console.log('1',this.bookList)           
          this.bookList.forEach((i,index)=>{
            // console.log(i)
            if(i.recur_server=="219.141.140.10"){
              i.recur_server="北京"
            }
            if(i.recur_server=="8.8.8.8"){
              i.recur_server="加州"
            }
            if(i.recur_server=="8.8.4.4"){
              i.recur_server="美国"
            }
            if(i.recur_server=="91.239.100.100"){
              i.recur_server="丹麦"
            }
            if(i.recur_server=="77.88.8.8"){
              i.recur_server="俄罗斯"
            }
            if(i.recur_server=="80.80.80.80"){
              i.recur_server="荷兰"
            }
            if(i.recur_server=="221.11.1.67"){
              i.recur_server="陕西"
            }
            if(i.recur_server=="210.22.70.3"){
              i.recur_server="上海"
            }
            if(i.recur_server=="79.141.82.250"){
              i.recur_server="瑞士"
            }
            if(i.recur_server=="61.132.163.68"){
              i.recur_server="安徽"
            }
            if(i.recur_server=="45.248.197.53"){
              i.recur_server="澳大利亚"
            }
            if(i.recur_server=="168.95.1.1"){
              i.recur_server="台湾"
            }
            if(i.recur_server=="202.14.67.4"){
              i.recur_server="香港"
            }
            if(i.recur_server=="210.22.70.3"){
              i.recur_server="上海"
            }
            if(i.recur_server=="45.248.197.5"){
              i.recur_server="澳大利亚"
            }
            if(i.recur_server=="168.95.1.1"){
              i.recur_server="台湾"
            }
            if(i.recur_server=="202.14.67.4"){
              i.recur_server="香港"
            }
            if(i.recur_server=="84.200.69.80"){
              i.recur_server="德国"
            }
            if(i.recur_server=="223.6.6.6"){
              i.recur_server="杭州"
            } 
            if(i.recur_server=="165.87.13.129"){
              i.recur_server="德州"
            } 
          }),
          $('#CDN').bootstrapTable({
            data: this.bookList
            })                        
          this.test();  
         })
    },
    btn:function(){
      // console.log(this.input)        
      var search = this.input;
      if (search) {
        this.searchData = this.bookList.filter(function(product) {
          // console.log('1',product)
          return Object.keys(product).some(function(key) {
            // console.log('2',key)
            return String(product['domain_name']).toLowerCase().indexOf(search) > -1
          })
        })
        $('#CDN').bootstrapTable("load", this.searchData)  
      }
      else{
        $('#CDN').bootstrapTable("load", this.bookList)  
      }          
      },
    init(){
			          let _this = this;
			          var container = document.getElementById("mynetwork");
			          var data = {
			            nodes: _this.nodes,
			            edges: _this.edges,
			          };		
			          _this.options = {
			            edges: {
			                    width: 3,
			                    length: 200,
			                    shadow: true,
			                    arrows: { 
			                      to: {
			                        enabled: true,
			                        scaleFactor: 1,  
			                        type: "arrow"
			                      },
                           }, 
                           color: {
			                      color: "#bc68e6",
			                      highlight: "yellow",
			                      hover: "#1fe1c6",
			                      inherit: "from",
			                      opacity: 1.0
			                    },
			                    font: {
			                      size: 14, 
			                      face: 'arial',
			                      background: 'white',
			                      strokeWidth: 10,
			                      strokeColor: 'rgb(112, 184, 240)',
			                      align: 'horizontal',
			                      multi: false,
			                      vadjust: 0,
			                      bold: {
			                        color: "green",
			                      },
			                   },
			            },
			            nodes: {
			              shape: 'image',
			              font: {
			                bold: {
			                  color: "red",
			                },
			              },
			            },
			            physics: {
			              enabled: false,
			            },
			            interaction: {
			              hover: true,
			              dragNodes: true, //是否能拖动节点
			              dragView: true, //是否能拖动画布
			              hover: true, //鼠标移过后加粗该节点和连接线
			              multiselect: true, //按 ctrl 多选
			              selectable: true, //是否可以点击选择
			              selectConnectedEdges: true, //选择节点后是否显示连接线
			              hoverConnectedEdges: true, //鼠标滑动节点后是否显示连接线
			              zoomView: true //是否能缩放画布
			            },
                  physics: {
                    enabled: true,
                    barnesHut: {
                        gravitationalConstant: -10000,
                        centralGravity: 0.3,
                        springLength: 120,
                        springConstant: 0.04,
                        damping: 0.09,
                        avoidOverlap: 0
                    }
                }
			          };
			       _this.network = new vis.Network(container, data,  _this.options);
          },
    test(){
      this.$http.get('http://127.0.0.1:8000/query/neo4j?domain=' + this.search)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
          console.log('10',res)
          this.vislist =res.neo4j_lists
          this.vislist[0].forEach((i,index)=>{
            // console.log(i)
            if(i.domain_name){
              this.nodes[index]={id:i.id,label:i.domain_name,image:'http://sunhanwu.top:8090/upload/2020/12/%E5%9F%9F%E5%90%8D-e2350ec15bc34b67b9150ad9e42cd96b.png'}
            }
            if(i.ip){
              this.nodes[index]={id:i.id,label:i.ip,image:'http://sunhanwu.top:8090/upload/2020/12/ip-632484e476674fc3a433d747c6ae01f0.png'}
            }
          })
           console.log(this.nodes)      
          this.vislist[1].forEach((i,index)=>{
            // console.log(i)
          this.edges[index] = {from: i['from'],to: i['to'], label:i['label']}
          }) 
        this.init();
      })
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
  .mynetwork {
			  height: 800px;
			  border: 0px solid lightgray;
			  canvas{
			    cursor: pointer;
			  }
		}
</style>