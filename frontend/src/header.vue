<template>
    <div class="header-wrapper" style="display: flex">
      <Logo />
      <div style="display: flex; justify-content: space-between; width: 100%; flex-wrap: wrap;">

        <div class="nav nav-pills" style="margin-left:50px; display: flex; align-items: center" v-if="is_admin || is_super_admin">
            <router-link v-if="is_admin" to="/admin/dashboard">
              <span :class="['nav-link', {'active': $route.path === '/admin/dashboard' || $route.path === '/admin/dashboard'}]"><i class="fa fa-bar-chart"></i>Dashboard</span>
            </router-link>
            <router-link v-if="is_admin" to="/admin/wallets">
              <span :class="['nav-link', {'active': $route.path === '/admin/wallets'}]"><i class="fa fa-check"></i> Verified wallets</span>
            </router-link>
            <router-link v-if="is_super_admin" :to="{name: 'superadmin'}">
              <span :class="['nav-link', {'active': $route.name === 'superadmin'}]"><i class="fa fa-check"></i> Super Admin</span>
            </router-link>
        </div>

        <div></div>

        <div>
          <div>
            <b-button v-on:click="connect_wallet()" :class="{'connected': wallet_address}" variant="primary" id="wallet-connect">
              <img v-if="wallet_address"  height="30" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/MetaMask_Fox.svg/1024px-MetaMask_Fox.svg.png?20220831120339"/>
              {{wallet_address_concat}}
            </b-button>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import Logo from './logo';
    export default {
      components: {
        Logo,
      },

      data() {
        return {
        };
      },

      computed: {
        wallet_address() {
          return this.$store.state.user?.user?.wallet?.address;
        },
        is_connected() {
          return this.$store.state.user.user.wallet != null;
        },
        wallet_address_concat() {
            if (this.is_connected) {
                return `${this.wallet_address.slice(0, 6) + '...' + this.wallet_address.slice(-4)}`;
            }
            return 'Connect wallet';
        },
        is_verified() {
            return this.is_connected;
        },
        is_admin() {
            return this.$store.state.user.user?.organizations?.length > 0;
        },
        is_super_admin() {
            return this.$store.state.user.user.is_super_admin
        },
        contextId() {
          return this.$route.params.context_id || null;
        },
        orgId() {
          return this.$route.params.org_id || null;
        }
  
      },
      methods: {
        async connect_wallet() {
            const user = await this.$store.state.user.tokenCheck.connectWallet();
            if (user) {
                this.$store.commit('setUser', user);
            }
        },
      },
    };
  </script>
  <style scoped>
  div.web3modal-modal-card, div.web3modal-modal-card {
    z-index: 9999999 !important;
  }
    #wallet-connect.connected {
    background-color:#2b2b2b !important;
    border: 1px solid #fff !important;
    padding:15px 30px 15px 30px !important;
    color:#FFF; font-size:1.2em;
    font-weight:bold;
  }
  #wallet-connect.connected img {
    margin-right:15px;
  }

  #wallet-connect {
    background-color:#f77b00 !important;
    border: 1px solid #fff !important;
    padding:15px 30px 15px 30px !important;
    color:#FFF; font-size:1.2em;
    font-weight:bold;
  }
  </style>
  