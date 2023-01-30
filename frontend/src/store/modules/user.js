import {LocalStorageBackend, TokenCheck} from "@/tokencheck";

export const user = {
    state: {
        user: {},
        tokenCheck: new TokenCheck(process.env.VUE_APP_BACKEND_URL, LocalStorageBackend),
    },
    getters: {

    },
    actions: {

    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        }
    }
};