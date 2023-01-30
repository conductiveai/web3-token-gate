import Vue from 'vue';
import Vuex from 'vuex';
import 'es6-promise/auto';
import layout from './modules/layout';
import { user } from "./modules/user";
import menu from "@/store/modules/menu";

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
    },
    actions: {
      setLang ({ commit }, payload) {
        commit('changeLang', payload);
      }
    },
    modules: {
      layout,
      menu,
      user
    }
});

