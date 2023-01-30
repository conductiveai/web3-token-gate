<template>
  <div>
    <div class="page-wrapper" :class="layoutobj">
      <div class="page-header">
        <Header />
      </div>
      <div class="page-body-wrapper">
        <div class="bg-overlay" :class="{active: activeoverlay }" @click="removeoverlay()"></div>
        <div class="page-body" style="padding-bottom: 63px; min-height: calc(100vh - 106px);" @click="hidesecondmenu()">
          <transition name="fadeIn" enter-active-class="animated fadeIn">
           <router-view class="view"></router-view>
          </transition>
        </div>
        <Footer/>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { layoutClasses } from '../constants/layout';
  import Header from '../header';
  import Footer from './footer';
  export default {
    name: 'mainpage',
    components:{
      Header,
      Footer,
    },
    data(){
      return{
        mobileheader_toggle_var: false,
        horizontal_Sidebar: true,
        resized:false,
        layoutobj:{}
      };
    },
    computed: {
      ...mapState({
        layout: state => state.layout.layout,
        activeoverlay: (state) => state.menu.activeoverlay
      }),
      layoutobject: {
        get: function () {
          return JSON.parse(JSON.stringify(layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout)))[this.layout.settings.layout];
        },
        set: function () {
          this.layoutobj = layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout);
          this.layoutobj = JSON.parse(JSON.stringify(this.layoutobj))[this.layout.settings.layout];
          return this.layoutobj;
        }
      }
    },
    watch:{
      '$route' (){
        this.layoutobj = layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout);
        if((window.innerWidth < 991 && this.layout.settings.layout === 'LosAngeles') || (window.innerWidth < 991 && this.layout.settings.layout === 'Singapore') || (window.innerWidth < 991 && this.layout.settings.layout === 'Barcelona')) {
          const newlayout = JSON.parse(JSON.stringify(this.layoutobj).replace('horizontal-wrapper', 'compact-wrapper'));
          this.layoutobj = JSON.parse(JSON.stringify(newlayout))[this.layout.settings.layout];
        } else  {
          this.layoutobj = JSON.parse(JSON.stringify(this.layoutobj))[this.layout.settings.layout]; 
        }
      },
      sidebar_toggle_var: function (){
        this.resized = (this.width <= 991) ? !this.sidebar_toggle_var : this.sidebar_toggle_var;      
      }
    },
    created(){
      window.addEventListener('resize', this.handleResize);
      this.handleResize();
      this.resized = this.sidebar_toggle_var;
      this.$store.dispatch('layout/set');
      this.layout.settings.layout = this.$route.query.layout? this.$route.query.layout : 'Barcelona';
      this.layoutobj = layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout);
      this.layoutobj = JSON.parse(JSON.stringify(this.layoutobj))[this.layout.settings.layout]; 
      document.body.classList.add('dark-only');
    },
    methods:{
      handleResize() {
        this.$store.dispatch('menu/resizetoggle');
      },
      removeoverlay() {
        this.$store.state.menu.activeoverlay = false;
        if(window.innerWidth < 991){  
          this.$store.state.menu.togglesidebar = false; 
        }
        this.menuItems.filter(menuItem => {
          menuItem.active = false;
        });
      }, 
      hidesecondmenu() {
        if(this.layoutobject.split(' ').includes('compact-sidebar')) {
          this.menuItems.filter(menuItem => {
            menuItem.active = false;
          });
        }
        if(window.innerWidth < 991) {
          this.$store.state.menu.togglesidebar = false; 
        }
      }
    }
  };
</script>

