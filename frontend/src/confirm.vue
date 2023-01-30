<template>
  <div>
    <div v-if="!context && contextNotFound">
    <h4 class="text-center m-t-50">Contract not found</h4>
    </div>
    <div v-else-if="!context && !contextNotFound">
      <h4 class="text-center m-t-50">Loading...</h4>
    </div>
    <div v-else>
      <div id="background"></div>
      <b-modal id="modal" centered title="Modal Title" ok-title="Save Changes" class="theme-modal light-only">
        <p>Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.</p>
      </b-modal>
      <!-- Container-fluid starts-->
      <div class="container-fluid" style="padding-top:30px;">
        <div class="edit-profile">
          <div class="row">
            <!--

            -->
            <div class="col-xl-4" :key="formDisabled">
              <div id="address-form" style="height: 100%" :class="{disabled: formDisabled, 'border-highlight': has_balance}" class="card">
                <div class="card-header">
                  <h4 class="card-title mb-0" style="color:#99f868">
                    {{ formTitle }}

                  </h4>
                  <div class="card-options"><a class="card-options-collapse" href="#" data-toggle="card-collapse"><i class="fe fe-chevron-up"></i></a><a class="card-options-remove" href="#" data-toggle="card-remove"><i class="fe fe-x"></i></a></div>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label class="form-label">First name</label>
                        <input v-model="form.first_name" class="form-control" type="text" placeholder="Vitalik">
                      </div>
                    </div>
                    <div class="col-sm-6 col-md-6">
                      <div class="form-group">
                        <label class="form-label">Last name</label>
                        <input v-model="form.last_name" class="form-control" type="text" placeholder="Buterin">
                      </div>
                    </div>
                    <div class="col-sm-12 col-md-12">
                      <div class="form-group">
                        <label class="form-label">Phone Number</label>
                        <input v-model="form.phone" class="form-control" type="text" placeholder="+1 (555) 555-1234">
                      </div>
                    </div>

                    <div class="col-sm-12 col-md-12">
                      <div class="form-group">
                        <label class="form-label">Email address</label>
                        <input v-model="form.email" class="form-control" type="text" placeholder="vitalik@ethereum.org">
                      </div>
                    </div>
                    <div class="col-sm-12 col-md-12">
                      <div class="form-group">
                        <label class="form-label">Address 1</label>
                        <input v-model="form.address1" class="form-control" type="text" placeholder="1234 Ethereum Rd.">
                      </div>
                    </div>
                    <div class="col-md-12">
                      <div class="form-group">
                        <label class="form-label">Address 2</label>
                        <input v-model="form.address2" class="form-control" type="text" placeholder="Floor #2">
                      </div>
                    </div>
                    <div class="col-md-12">
                      <div class="form-group">
                        <label class="form-label">Address 3</label>
                        <input v-model="form.address3" class="form-control" type="text" placeholder="">
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label class="form-label">City</label>
                        <input v-model="form.city" class="form-control" type="text" placeholder="Alberta">
                      </div>
                    </div>
                    <div class="col-sm-6 col-md-6">
                      <div class="form-group">
                        <label class="form-label">STATE or PROVINCE (Where Applicable)</label>
                        <input v-model="form.region" class="form-control" type="text" placeholder="B.C.">
                      </div>
                    </div>
                    <div class="col-sm-6 col-md-6">
                      <div class="form-group">
                        <label class="form-label">Postal Code</label>
                        <input v-model="form.postal_code" class="form-control" placeholder="ABC123">
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label class="form-label">Country</label>
                        <select v-model="form.country" class="form-control btn-square">
                          <option value="0">--Select--</option>
                          <option value="Singapore">Singapore</option>
                          <option value="Malaysia">Malaysia</option>
                          <option value="Australia">Australia</option>
                          <option value="Japan">Japan</option>
                          <option value="Korea">Korea</option>
                          <option value="US">US</option>
                          <option value="Germany">Germany</option>
                          <option value="UK">UK</option>
                          <option value="Philippines">Philippines</option>
                          <option value="Hong Kong">Hong Kong</option>
                        </select>
                      </div>
                    </div>
                    <div v-if="form.sizes.length" class="col-12">
                      <table class="table">
                        <thead>
                        <tr>
                          <th>Token ID</th>
                          <th class="text-center">Size</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="sizes in form.sizes" :key="sizes.token_id">
                          <td>#{{ sizes.token_id}}</td>
                          <td>
                            <table class="table table-borderless">
                              <tr v-for="size_index in sizes.sizes.length" :key="size_index">
                                <td>
                                  <p class="text-center">{{ size_index }}.</p>
                                </td>
                                <td>
                                  <select class="form-control btn-square" v-model="sizes.sizes[size_index - 1]">
                                    <option :value="null">--Select--</option>
                                    <option value="S">S</option>
                                    <option value="M">M</option>
                                    <option value="L">L</option>
                                    <option value="XL">XL</option>
                                  </select>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                        </tbody>

                      </table>
                    </div>
                  </div>
                </div>
                <div class="card-footer text-right">
                  <p style="color: #e52626; padding-top: 10px">{{ formError }}</p>
                  <SpinnerButton :busy="profileSubmitting" class="btn btn-primary" :disabled="!has_balance || profileSubmitting"  v-on:click="submit_address()" style="background-color:#99f868 !important; border: 1px solid #fff; padding:20px 50px 20px 50px !important; color:#070d1f; font-size:1.5em; font-weight:bold">
                    {{ profileSubmitting ? 'Updating' : (profileExists ? 'Update Profile': 'Complete profile') }}
                  </SpinnerButton>
                </div>
              </div>
            </div>
            <div class="col-xl-8">
              <div style="height: 100%">
                <div class="row" style="height: 100%">

                  <div class="col-xl-12" style="height: 100%">
                    <div id="card-message" style="height: 100%" class="card border-highlight" :class="{'border-highlight': !is_verified, disabled: is_verified}">
                      <div class="card-body" style="height: 100%">

                        <div class="row text-center">
                          <div class="col-xl-12">

                            <h1 id="header-msg" style="margin-top:20px;" v-html="titleText"></h1>

                            <p v-if="context">
                              {{ context?.contract?.token_name }}
                              @
                              {{ context?.organization?.name }}
                            </p>

                            <p style="padding-top:50px;">
                              <img :src="context.image || 'https://media2.giphy.com/media/2jH4fJ4i4TLFyaFucI/giphy.gif?cid=ecf05e47wci4jltwosdbu1f6gxsf21c6mhwssi91cbc0w6rf&rid=giphy.gif&ct=g'" height="400"/>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-xl-9 xl-100 box-col-12">

                  <div class="col-md-12">


                  </div>
                </div>

              </div>
            </div>



          </div>
        </div>
      </div>
      <!-- Container-fluid Ends-->
    </div>
  </div>
</template>
<style scoped>
input.form-control {
  background-color:#8492af !important;
  color:#070d1f;
  font-size:larger;
  font-weight: bold;
}
.border-highlight {
  border-color: #99f868 !important;
}
</style>
<script>

import SpinnerButton from "@/components/spinnerbutton.vue";

const primary = "#aef07a";
const secondary = localStorage.getItem("secondary_color") || "#f73164";


export default {
  components: {SpinnerButton},
  computed: {
    is_verified() {
      return this.is_connected;
    },
    formTitle() {
      if (this.context.title) {
        return this.context.title;
      }
      return "Confirm your details"
    },
    formDisabled() {
      return !this.has_balance || this.profileSubmitting
    },

    has_balance() {
      if (this.context?.token_id_whitelist?.length) {
        if (!this.context.token_id_whitelist.some((token_id) => this.balancesByToken[token_id] > 0)) {
          return false;
        }
      }
      return this.is_verified && this.context && this.balance >= this.context.threshold;
    },
    context_uuid() {
      return this.$route.params.context_id;
    },
    is_connected() {
      return this.$store.state.user?.user?.wallet != null;
    },
    wallet_address() {
      return this.$store.state.user.user.wallet.address;
    },
    titleText() {
      if (this.is_verified) {
        if (!this.profileExists) {
          if (this.has_balance) {
            return this.fillTemplate((this.context.texts.accepted || `👈 Great anon, you have {balance} token(s). Complete the form.`));
          } else if (this.context) {
            return this.fillTemplate((this.context.texts.not_accepted || `You need {balance} token(s) to participate.`));
          } else {
            return 'Loading...'
          }
        }
        return this.fillTemplate(this.context.texts.completed || `👍 Great anon, you have completed your profile.`);
      }
      return this.fillTemplate(this.context.texts.greeting || '👋 Hey anon. Prove you\'re a holder, connect you wallet');
    },
    user() {
      return this.$store.state.user.user;
    },
    tokenCheck() {
      return this.$store.state.user.tokenCheck;
    },
  },

  methods: {

    fillTemplate(string) {
      return string
          .replace("{balance}", this.balance)
          .replace("{threshold}", this.context.threshold)
          .replace("{claimable_balance}", this.relevantBalance);
    },

    async submit_address() {

      if (!this.is_verified) {
        alert("Please connect and verify your wallet address");
        return;
      }
      const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-1]\d{2}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (emailRegex.test(this.form.email) === false) {
        alert("Please enter a valid email address");
        return;
      }

      //validate these fields
      if (
          this.form.first_name === "" ||
          this.form.last_name === "" ||
          this.form.email === "" ||
          this.form.phone === "" ||
          this.form.address1=== "" ||
          this.form.city === "" ||
          this.form.region === "" ||
          this.form.postal_code === "" ||
          this.form.country === "0"
      ) {
        alert("Please fill out all fields");
        return;
      }
      for (let size of this.form.sizes) {
        if (size.sizes.includes(null)) {
          this.formError = "Please specify all sizes"
          return;
        }
      }

      this.profileSubmitting = true;
      try {
        const {profile, message} = await this.tokenCheck.sendContact(this.form, this.context_uuid, this.profileExists);
        this.formError = "";
        if(profile) {
          alert(message);

          //redirect
          // window.location.href = "...";
        }
      } catch (e){
        this.formError = e.message;
      }
      this.profileSubmitting = false;
    },

  },
  data() {
    return {
      context: null,
      contextNotFound: false,
      profileSubmitting: false,
      balancesByToken: {},
      balance: 0,
      relevantBalance: 0,
      formError: "",
      form: {
        first_name: "",
        last_name: "",
        phone: "",
        email: "",
        address1: "",
        address2: "",
        address3: "",
        city: "",
        region: "",
        postal_code: "",
        country: "0",
        sizes: [],
      },
      profileExists: false,
    };
  },
  watch: {

    form: {
      handler() {
        if (this.form.address1.length > 30) {
          this.form.address1 = this.form.address1.substring(0, 30);
        }
        if (this.form.address2.length > 30) {
          this.form.address2 = this.form.address2.substring(0, 30);
        }
        if (this.form.address3.length > 30) {
          this.form.address3 = this.form.address3.substring(0, 30);
        }
      },
      deep: true,
    },

    user: {
      async handler() {
        const { profile, balance, relevant_balance } = await this.tokenCheck.getProfile(this.context_uuid);
        this.balance = balance;
        this.relevantBalance = relevant_balance
        if (profile) {
          this.form = profile;
          this.profileExists = true;
        }
      },
      immediate: true
    },
    async context() {
      if (!this.context?.token_id_whitelist?.length) {
        return;
      }

      // if context restricts token ids, get user balances for those
      const balances = await this.tokenCheck.getBalances(this.context_uuid);

      // update balances
      this.balancesByToken = {}
      for (const balance of balances) {
        this.balancesByToken[balance.token_id] = balance.balance;
      }

      // if user already has a profile, avoid empty sizes initialization
      if (this.form.sizes.length > 0) {
        return;
      }

      // initialize sizes
      for (const balance of balances) {
        this.form.sizes.push({
          token_id: balance.token_id,
          sizes: Array.from({length: balance.balance}, () => null),
        })
      }
    },
  },
  async created() {
    this.$store.commit("menu/setLoading", true);
    try {
      this.context = await this.tokenCheck.getContext(this.context_uuid);
      this.contextNotFound = false;
    } catch (e) {
      this.contextNotFound = true;
    }
    this.$store.commit("menu/setLoading", false);
  }
};
</script>
<style>
div#admin-page div.card {
  border: none !important;

}

div#admin-page div.card-body, div#admin-page div.card-header, div#admin-page div.card-footer, div#admin-page div.card, div#admin-page footer.footer {
  background-color:#272931 !important;
}

body, body.dark-only, div#admin-page div#admin-page div.page-wrapper, div#admin-page div.page-body-wrapper, div#admin-page div.page-body, div#admin-page div.page {
  background-color:#1c1d24 !important;
}

div#admin-page form.card, div#admin-page div.card {
  background: transparent !important;

}

form.card, div.card, div.card-footer {
  background: #272931 !important;

}
</style>
