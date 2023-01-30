<template>
  <div class="text-center" style="margin-top: 40vh;" v-if="!$store.state.user.user.is_super_admin">
    Verifying...
  </div>
  <div v-else class="d-flex justify-content-center">
    <div style="margin-top:30px; max-width: 1000px" class="d-flex justify-content-center">
      <BModal ref="editorModal" @ok="e => {e.preventDefault(); saveContextEdits()}" title="Edit Token Form" v-if="editedContract" id="modal-editor">
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label">Form Title</label>
              <input class="form-control" v-model="editedContract.title">
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label">Image URL</label>
              <input class="form-control" v-model="editedContract.image">
            </div>
          </div>
          <div class="col-md-12">
            <div class="form-group">
              <label class="form-label">Threshold</label>
              <input class="form-control" type="number" step="1" min="1" v-model="editedContract.threshold">
            </div>
          </div>

          <div class="col-md-12">
            <h6>String templates</h6>
            <p>put <code>{balance}</code>, <code>{threshold}</code> or <code>{claimable_balance}</code> in templates where needed (balance not accessible in greeting)</p>
          </div>

          <div class="col-md-12">
            <div class="form-group">
              <label class="form-label">Greeting Text</label>
              <input class="form-control" v-model="editedContract.texts.greeting">
            </div>
          </div>

          <div class="col-md-12">
            <div class="form-group">
              <label class="form-label">Accepted Text</label>
              <input class="form-control" v-model="editedContract.texts.accepted">
            </div>
          </div>

          <div class="col-md-12">
            <div class="form-group">
              <label class="form-label">Not Accepted Text</label>
              <input class="form-control" v-model="editedContract.texts.not_accepted">
            </div>
          </div>

          <div class="col-md-12">
            <div class="form-group">
              <label class="form-label">Completed Text</label>
              <input class="form-control" v-model="editedContract.texts.completed">
            </div>
          </div>

          <div class="col-md-12">
            <h6>Token Whitelist</h6>
          </div>

          <div class="col-12">
            <label class="form-label">Token IDs</label>
            <table class="table">
              <tr v-for="tokenID in editedContract.token_id_whitelist">
                <td>
                  <code> {{ tokenID }} </code>
                </td>
                <td>
                  <BBtn @click="removeTokenIdFromEditedContract(tokenID)"> Remove </BBtn>
                </td>
              </tr>
              <tr v-if="!editedContract.token_id_whitelist.length">
                <td class="text-center text-white" colspan="2">No Token IDs currently whitelisted</td>
              </tr>
              <tr>
                <td>
                  <input ref="tokenIdEditWhitelist" class="form-control" type="number" step="1" min="1" placeholder="Token ID" @keydown.enter="addTokenIdToEditedContract">
                </td>
                <td>
                  <BBtn @click="addTokenIdToEditedContract"> Whitelist Token ID </BBtn>
                </td>
              </tr>
            </table>
          </div>

          <div class="col-12">
            <p style="color: #e52626; padding-top: 10px">{{ editContextError }}</p>
          </div>
        </div>
      </BModal>

      <div class="container-fluid" id="admin-page">
        <div class="row">
          <div class="col">
            <div class="default-according style-1 faq-accordion job-accordion" id="accordionoc">
              <div class="row">
                <div class="col-xl-12">
                  <b-card no-body>
                    <b-card-header header-tag="div" role="tab">
                      <div class="row">
                        <div class="col-md-12 d-flex" style="justify-content: space-between">
                          <h6 style="margin-top:15px;">Select Organization</h6>
                          <div class="card-header-right-icon">
                            <select v-model="selectedOrg" class="button btn btn-secondary">
                              <option v-for="organization in organizations" :value="organization" :key="organization.id">{{ organization.name }}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </b-card-header>
                  </b-card>
                </div>
              </div>
            </div>
          </div>
          <div class="col-12">
            <div class="card" style="border-radius:15px !important;">
              <div class="card-header">
                <div class="d-flex" style="justify-content: space-between">
                  <h4 class="card-title mb-0">Organization Details: {{ selectedOrg?.name }}</h4>
                  <button class="btn btn-danger" @click="disableOrg">Disable Organization</button>
                </div>
                <a v-if="selectedOrg !== null" :href="`${location.origin}/admin/o/${selectedOrg.id}`">{{`/admin/o/${selectedOrg.id}`}}</a>
              </div>
              <div class="card-body" v-if="selectedOrg === null">
                <p class="text-center">Please select an organization</p>
              </div>
              <div v-else class="card-body">
                <div class="row">
                  <!-- Admins of selected Organization -->
                  <div class="col-md-12 p-b-40">
                    <div class="form-group border p-20">
                      <h4>Admins</h4>
                      <p v-if="selectedOrg.admins.length === 0">
                        No admins in given organization
                      </p>
                      <table v-else class="table">
                        <tr v-for="admin in selectedOrg.admins" :key="admin.id">
                          <td>{{ admin.address }}</td>
                          <td class="d-flex justify-content-end"><button class="btn btn-danger" @click="removeAdmin(admin)">Remove</button></td>
                        </tr>
                      </table>
                      <h5>Add Admin</h5>
                      <div class="row">
                        <div class="col-md-6 col-lg-9">
                          <input class="form-control" v-model="adminInput2" @keyup.enter="addAdmin" type="text" placeholder="Add Admin">
                        </div>
                        <div class="col-md-6 col-lg-3">
                          <button class="button btn btn-block btn-secondary" @click="addAdmin">Add Admin</button>
                        </div>
                        <div class="col-12">
                          <p style="color: #e52626; padding-top: 10px">{{ addAdminError }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Contracts of selected Organization -->
                  <div class="col-md-12">
                    <div class="form-group border p-20">
                      <h4>Contracts</h4>
                      <p v-if="selectedOrg.contexts.length === 0">
                        No contracts in given organization
                      </p>
                      <table v-else class="table">
                        <thead>
                        <tr>
                          <th>Name</th>
                          <th>Threshold</th>
                          <th>Verification URL</th>
                          <th></th>
                          <th></th>
                        </tr>
                        </thead>
                        <tr v-for="context in selectedOrg.contexts">
                          <td>
                            <a :href="`${location.origin}/t/${context.uuid}`">{{ context.title || context.contract.token_name || context.contract.address }}</a>
                          </td>
                          <td class="text-center">{{ context.threshold }}</td>
                          <td><CopyBtn label="Copy URL" :text="`${location.origin}/t/${context.uuid}`" /></td>
                          <td><BBtn v-b-modal.modal-editor variant="primary" @click="setEditingContext(context)" class="text-nowrap"><i class="fa fa-edit"></i>Edit</BBtn></td>
                          <td class="d-flex text-nowrap justify-content-end"><button class="btn btn-danger" @click="removeContext(context)"><i class="fa fa-trash"></i></button></td>
                        </tr>
                      </table>

                      <div class="row">

                        <div class="col-md-12">
                          <h5>Add Contract</h5>
                        </div>
                        <div class="col-md-6">
                          <div class="form-group">
                            <label class="form-label">Form Name</label>
                            <input v-model="createContract.title" class="form-control" type="text" placeholder="My Form">
                          </div>
                        </div>
                        <div class="col-md-6">
                          <div class="form-group">
                            <label class="form-label">Image URL</label>
                            <input v-model="createContract.image" class="form-control" type="text" placeholder="https://example.com/image.png">
                          </div>
                        </div>
                        <div class="col-md-5">
                          <div class="form-group">
                            <label class="form-label">Contract Address</label>
                            <input v-model="createContract.address" class="form-control" type="text" placeholder="0x0000000000000000000000000000000000000000">
                          </div>
                        </div>
                        <div class="col-md-3">
                          <div class="form-group">
                            <label class="form-label">Token Threshold</label>
                            <input class="form-control" placeholder="Token Threshold (Optional)" min="1"
                                   step="1" type="number" v-model="createContract.threshold">
                          </div>
                        </div>


                        <div class="col-md-4">
                          <div class="form-group">
                            <label class="form-label">Contract Chain</label>
                            <b-select v-model="createContract.chain">
                              <b-select-option v-for="chain in chainOptions" :value="chain.value" :key="chain.value">{{ chain.text }}</b-select-option>
                            </b-select>
                            <!--                          <select v-model="createContract.chain" class="button btn btn-block btn-secondary" type="text" placeholder="Ethereum">-->
                            <!--                            <option v-for="chain in chainOptions" :value="chain.value" :key="chain.value">{{ chain.text }}</option>-->
                            <!--                          </select>-->
                          </div>
                        </div>

                        <div class="col-md-8">
                          <div class="form-group">
                            <input @keydown.enter="addTokenID" class="form-control" placeholder="Token ID" min="1"
                                   step="1" type="number" v-model="tokenIDInput">
                          </div>
                        </div>


                        <div class="col-md-4">
                          <div class="form-group">
                            <button class="btn btn-block button btn-primary" @click="addTokenID">Add Token ID</button>
                          </div>
                        </div>
                        <div class="col-12">
                          <table class="m-t-10 table">
                            <tr v-for="(tokenID, i) in createContract.token_id_whitelist" :key="tokenID">

                              <td>{{i + 1}}) {{ tokenID }} </td>

                              <td class="d-flex justify-content-end"><button class="btn btn-danger" @click="removeTokenID(tokenID)">Remove</button></td>
                            </tr>
                          </table>
                        </div>
                        <div class="col-md-12">
                          <b-btn class="button btn-block" @click="addContract">Add Contract To Organization</b-btn>
                          <p style="color: #e52626; padding-top: 10px">{{ addContractError }}</p>
                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer text-right">
              </div>
            </div>
          </div>

          <div class="col-12">

            <div class="card" style="border-radius:15px !important;">
              <div class="card-header">
                <h4 class="card-title mb-0">Register Organization</h4>
              </div>

              <div class="card-body">
                <div class="row">
                  <div class="col-md-12">
                    <div class="form-group">
                      <label class="form-label">Name</label>
                      <input v-model="registerOrgData.name" class="form-control" type="text" placeholder="Organization Name">
                    </div>
                  </div>
                  <div class="col-md-12">
                    <div class="form-group">
                      <label class="form-label">Admins: {{ registerOrgData.admins.length }} selected</label>
                      <div class="row">
                        <div class="col-md-6 col-lg-9">
                          <input class="form-control" v-model="adminInput" @keyup.enter="addAdminToCreatedOrg" type="text" placeholder="Admin wallet address">
                        </div>
                        <div class="col-md-6 col-lg-3">
                          <button class="button btn btn-block btn-secondary" @click="addAdminToCreatedOrg">Add Admin</button>
                        </div>
                      </div>

                      <table class="m-t-10 table">
                        <tr v-for="(admin, i) in registerOrgData.admins" :key="admin">

                          <td>{{i + 1}}) {{ admin }} </td>

                          <td class="d-flex justify-content-end"><button class="btn btn-danger" @click="registerOrgData.admins.splice(i, 1)">Remove</button></td>
                        </tr>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer d-flex justify-content-between">
                <p style="color: #e52626; padding-top: 10px">{{ addOrgError }}</p>
                <button class="btn btn-primary" @click="registerOrg">Register</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import CopyBtn from "@/components/copybtn.vue";
import ContextEditor from "@/components/contexteditor.vue";

export default {
  name: "superadmin",
  components: {
    ContextEditor,
    CopyBtn

  },
  setup() {
    return {
      location: window.location,
      standards: [
        {
          name: 'ERC-20',
          value: 20
        },
        {
          name: 'ERC-721',
          value: 721
        },
        {
          name: 'ERC-1155',
          value: 1155
        }
      ]
    }
  },
  watch: {
    threshold() {
      if (this.createContract.threshold === null || this.createContract.threshold === "") {
        this.createContract.threshold = null;
        return;
      }

      this.createContract.threshold = Math.floor(this.threshold);
      if (this.createContract.threshold <= 0) {
        this.createContract.threshold = 1;
      }
    },
    tokenIDInput() {
      if (this.tokenIDInput === null || this.tokenIDInput === "") {
        this.tokenIDInput = null;
        return;
      }

      this.tokenIDInput = Math.floor(this.tokenIDInput);
      if (this.tokenIDInput < 0) {
        this.tokenIDInput = 0;
      }
    }
  },
  methods: {

    addTokenIdToEditedContract() {
      let newTokenId = this.$refs.tokenIdEditWhitelist.value;
      if (!this.editedContract.token_id_whitelist.includes(newTokenId)) {
        this.editedContract.token_id_whitelist.push(newTokenId);
      }
      this.$refs.tokenIdEditWhitelist.value = "";
    },
    removeTokenIdFromEditedContract(tokenID) {
      this.editedContract.token_id_whitelist = this.editedContract.token_id_whitelist.filter(id => id !== tokenID);
    },

    addAdminToCreatedOrg() {
      this.registerOrgData.admins.push(this.adminInput);
      this.adminInput = "";
    },

    addTokenID() {
      if (this.tokenIDInput === null || this.tokenIDInput === "") {
        return;
      }

      if (this.createContract.token_id_whitelist.includes(this.tokenIDInput)) {
        this.tokenIDInput = "";
        return;
      }

      this.createContract.token_id_whitelist.push(this.tokenIDInput);
      this.tokenIDInput = "";
    },

    setEditingContext(contract) {
      this.editedContract = JSON.parse(JSON.stringify(contract));
    },

    removeTokenID(tokenID) {
      this.createContract.token_id_whitelist = this.createContract.token_id_whitelist.filter(id => id !== tokenID);
    },

    async disableOrg() {
      await this.tokenCheck.disableOrg(this.selectedOrg.id);
      alert("Organization disabled");
      this.organizations = await this.tokenCheck.listOrgs();
      this.selectedOrg = this.organizations[this.organizations.length - 1];
    },

    async addAdmin() {
      try {
        await this.tokenCheck.addAdmin(this.adminInput2, this.selectedOrg.id);
      } catch (e) {
        this.addAdminError = e.message;
        return;
      }
      this.addAdminError = "";
      await this.refreshSelectedOrg();
      this.adminInput2 = "";
    },

    async saveContextEdits() {
      try {

        if (this.editedContract.image === "") {
          this.editedContract.image = null;
        }

        await this.tokenCheck.editContext(this.editedContract.uuid, this.editedContract);
        this.editContextError = "";
        this.$refs.editorModal.hide();
        await this.refreshSelectedOrg();
      } catch (e) {
        this.editContextError = e.message;
      }
    },
    async addContract() {
      this.addTokenID();
      try {
        await this.tokenCheck.addContract(this.createContract, this.selectedOrg.id);
      } catch (e) {
        this.addContractError = e.message;
        return;
      }

      this.addContractError = "";
      await this.refreshSelectedOrg();
      this.createContract = {
        address: "",
        chain: 1,
        threshold: null,
      };
    },

    async removeAdmin(wallet) {
      await this.tokenCheck.removeAdmin(wallet.address, this.selectedOrg.id);
      await this.refreshSelectedOrg();
    },

    async removeContext(context) {
      await this.tokenCheck.removeContext(context.uuid);
      await this.refreshSelectedOrg();
    },

    copyText(text) {
      navigator.clipboard.writeText(text);
    },

    async registerOrg() {
      try {
        await this.tokenCheck.createOrg(this.registerOrgData);
      } catch (e) {
        this.addOrgError = e.message;
        return;
      }
      this.addOrgError = "";
      this.organizations = await this.tokenCheck.listOrgs();
      this.selectedOrg = this.organizations[this.organizations.length - 1];
      this.registerOrgData = {
        name: "",
        admins: [],
        contracts: [],
      };
    },
    async refreshSelectedOrg() {
      const org = this.organizations.find(org => org.id === this.selectedOrg.id);
      const updatedOrg = await this.tokenCheck.getOrg(org.id);
      Object.assign(org, updatedOrg);
    }
  },
  async created() {
    this.organizations = await this.tokenCheck.listOrgs();
    this.selectedOrg = this.organizations[0];
  },
  data() {
    return {
      adminInput: "",
      adminInput2: "",
      tokenIDInput: "",
      editedContract: null,
      editContextError: "",

      createContract: {
        address: '',
        chain: 1,
        name: '',
        standard: 20,
        threshold: 1,
        token_id_whitelist: [],
        title: null,
        image: null,
      },

      chainOptions: [
        { text: "Ethereum", value: 1 },
        { text: "Binance Smart Chain", value: 56 },
        { text: "Polygon", value: 137 },
      ],
      registerOrgData: {
        name: "",
        admins: [],
        contracts: [],
      },
      organizations: [
      ],
      selectedOrg: null,
      addContractError: "",
      addAdminError: "",
      addOrgError: "",
    }
  },
  computed: {
    tokenCheck() {
      return this.$store.state.user.tokenCheck;
    },
    threshold() {
      return this.createContract.threshold;
    }
  },
}
</script>

<style scoped>

</style>