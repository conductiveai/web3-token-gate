<template>
  <div>
    <orgprovider v-model="selectedOrg">
    </orgprovider>

    <div style="margin-top:30px;">
      <div class="container-fluid"  id="admin-page">
        <div class="row">
          <div class="col-xl-4 xl-40">
            <div class="default-according style-1 faq-accordion job-accordion" id="accordionoc">
              <div class="row">

                <div class="col-xl-12">
                  <b-card no-body>
                    <b-card-header header-tag="div" role="tab">
                      <div class="row">
                        <div class="col-md-3">
                          <h6 style="margin-top:15px;">Contract</h6>
                        </div>
                        <div class="col-md-9">
                          <div class="card-header-right-icon">
                            <select v-model="selectedContract" class="button btn btn-secondary">
                              <option v-for="contract in contracts" :value="contract" :key="contract.context_uuid">{{ contract.token_name }}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </b-card-header>
                    <b-collapse id="collapselocation" visible role="tabpanel">
                      <b-card-body class="animate-chk">
                        <div class="location-checkbox" style="max-height: 50vw; overflow-y: scroll;">
                          <label
                              v-for="profile in holders"
                              :key="profile.id"
                              class="d-block wallet-entry"
                              :class="{walletSelected: selectedProfile?.id === profile.id}"
                              for="chk-ani21"
                              @click="selectedProfile = profile"
                          >
                            <img src="https://cryptologos.cc/logos/polygon-matic-logo.png" height="15" style="margin-right:15px;"/>
                            {{ profile.wallet.address }}
                          </label>
                          <p v-if="holders?.length === 0">
                            No wallets found
                          </p>

                        </div>
                      </b-card-body>
                      <button class="btn btn-block btn-primary text-center" @click="downloadCSV()" type="button">Export CSV</button>
                    </b-collapse>
                  </b-card>
                </div>

              </div>
            </div>
          </div>
          <div class="col-xl-8 xl-60">

            <div class="card" style="border-radius:15px !important;">
              <div class="card-header">
                <h4 class="card-title mb-0">Profile Details</h4>
                <div class="card-options"><a class="card-options-collapse" href="#" data-toggle="card-collapse"><i class="fe fe-chevron-up"></i></a><a class="card-options-remove" href="#" data-toggle="card-remove"><i class="fe fe-x"></i></a></div>
              </div>
              <div class="card-body" v-if="selectedProfile.id == null">
                <p class="text-center">Please select a profile</p>
              </div>
              <div v-else class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label class="form-label">First name</label>
                      <input disabled v-model="selectedProfile.first_name" class="form-control" type="text" placeholder="Vitalik">
                    </div>
                  </div>
                  <div class="col-sm-6 col-md-6">
                    <div class="form-group">
                      <label class="form-label">Last name</label>
                      <input disabled v-model="selectedProfile.last_name" class="form-control" type="text" placeholder="Buterin">
                    </div>
                  </div>

                  <div class="col-sm-12 col-md-12">
                    <div class="form-group">
                      <label class="form-label">Email address</label>
                      <input disabled v-model="selectedProfile.email" class="form-control" type="text" placeholder="vitalik@ethereum.org">
                    </div>
                  </div>
                  <div class="col-sm-12 col-md-12">
                    <div class="form-group">
                      <label class="form-label">Address 1</label>
                      <input disabled v-model="selectedProfile.address1" class="form-control" type="text" placeholder="1234 Ethereum Rd.">
                    </div>
                  </div>
                  <div class="col-md-12">
                    <div class="form-group">
                      <label class="form-label">Address 2</label>
                      <input disabled v-model="selectedProfile.address2" class="form-control" type="text" placeholder="Floor #2">
                    </div>
                  </div>
                  <div class="col-md-12">
                    <div class="form-group">
                      <label class="form-label">Address 3</label>
                      <input disabled v-model="selectedProfile.address3" class="form-control" type="text" placeholder="Floor #2">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label class="form-label">City</label>
                      <input disabled v-model="selectedProfile.city" class="form-control" type="text" placeholder="Alberta">
                    </div>
                  </div>
                  <div class="col-sm-6 col-md-6">
                    <div class="form-group">
                      <label class="form-label">Region</label>
                      <input disabled v-model="selectedProfile.region" class="form-control" type="text" placeholder="B.C.">
                    </div>
                  </div>
                  <div class="col-sm-6 col-md-6">
                    <div class="form-group">
                      <label class="form-label">Postal Code</label>
                      <input disabled v-model="selectedProfile.postal_code" class="form-control" type="number" placeholder="ABC123">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label class="form-label">Country</label>
                      <input class="form-control" disabled v-model="selectedProfile.country">
                    </div>
                  </div>
                  <div class="col-12" v-if="selectedProfile.sizes.length">
                    <table class="table">
                      <thead>
                      <tr>
                        <th>Token ID</th>
                        <th>Sizes</th>
                      </tr>
                      </thead>
                      <tbody>
                        <tr v-for="token_sizes in selectedProfile.sizes">
                          <td>{{ token_sizes.token_id }}</td>
                          <td>
                            <table class="table table-borderless">
                              <tr v-for="(size, i) in token_sizes.sizes" :key="i">
                                <td>{{i + 1}}. {{ size }}</td>
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
                <!--              <button class="btn btn-primary" @click="saveContact()">Update Profile</button>-->
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Container-fluid Ends-->
    </div>
  </div>
</template>
<script>

import Orgprovider from "@/components/orgprovider.vue";

export default {
  components: {
    Orgprovider
  },

  data() {
    return {
      selectedOrg: null,
      contracts: [],
      selectedContract: null,
      selectedProfile: {},
      holders: [],
    }
  },

  async created() {
    if (this.user.context) {
      this.contracts = await this.tokenCheck.getContracts(this.user.context.organization.id);
      if (this.contracts.length) {
        this.selectedContract = this.contracts[0];
      }
    }
  },

  computed: {
    user() {
      return this.$store.state.user.user
    },
    tokenCheck() {
      return this.$store.state.user.tokenCheck
    }
  },

  methods: {
    downloadCSV() {
      this.tokenCheck.exportCSV(this.selectedContract.context_uuid);
    },
  },
  watch: {
    async selectedContract() {
      if (this.selectedContract) {
        this.holders = await this.tokenCheck.getHolders(this.selectedContract.context_uuid);
      } else {
        this.holders = [];
      }
    },
    selectedOrg: {
      handler: async function () {
        console.log("Selected org", this.selectedOrg)
        if (this.selectedOrg) {
          this.contracts = await this.tokenCheck.getContracts(this.selectedOrg.id)
          this.selectedContract = this.contracts[0]
        }
      },
      deep: true,
      immediate: true
    },
    async user() {
      if (!this.selectedOrg) return;

      this.contracts = await this.tokenCheck.getContracts(this.selectedOrg.id);
      if (this.contracts.length) {
        this.selectedContract = this.contracts[0];
      }
    },
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

form.card, div.card {
  background: #272931 !important;

}
.wallet-entry {
  padding: 10px;
  border-radius: 15px;
  text-overflow: ellipsis;
  overflow: hidden;
  width: 100%;
  white-space: nowrap;
}

.walletSelected {
  background-color: #636984 !important;
}
</style>
