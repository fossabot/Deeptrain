<script setup lang="ts">
import { redirect } from "@/assets/script/utils";
import { captchaSize } from "@/assets/script/user";
import Turnstile from "@/components/captcha/Turnstile.vue";
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import axios from "axios";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const error = ref<string>("");
const form = reactive({
  username: "",
  password: "",
  captcha: "",
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: 'Please input username', trigger: 'blur' },
    { min: 3, max: 14, message: 'Length should be 3 to 14', trigger: 'change' },
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 26, message: 'Length should be 6 to 26', trigger: 'change' },
  ],
  captcha: [
    { required: true, message: '', trigger: 'blur' },
  ],
})

async function submit() {
  await element.value?.validate((valid: boolean, _) => {
    if (!valid) return;
    if (valid) {  // trigger submit event
      loading.value = true;
      axios.post('login/', form)
        .then(function(response) {
          console.log(response);
          error.value = "";
        })
        .catch(function(err) {
          error.value = err.response ? err.response.data['message'] : err.message; //@ts-ignore
          window['turnstile']?.reset("#cf-captcha");
        })
        .finally(function() {
          loading.value = false;
        })
    }
  })
}
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain">
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>Sign in to Deeptrain</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-alert v-if="error" style="transform: translateY(-8px)" :closable="false" :title="error" type="error" show-icon />
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username" prop="username">
            <el-input v-model="form.username" type="text" minlength="3" maxlength="14" />
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password minlength="6" maxlength="26" />
          </el-form-item>
          <el-form-item prop="captcha">
            <keep-alive>
              <Turnstile :size="captchaSize" id="cf-captcha" v-model="form.captcha" />
            </keep-alive>
          </el-form-item>
          <el-button class="validate-button" @click="submit">Sign in</el-button>
        </el-form>
        <el-divider />
        <div class="oauth">
          <a @click="redirect('https://github.com')"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>GitHub</title><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></a>
          <a @click="redirect('https://gitee.com')"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Gitee</title><path d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.982 0 1.778-.796 1.778-1.778v-.296a.593.593 0 0 0-.592-.593h-4.15a.592.592 0 0 1-.592-.592v-1.482a.593.593 0 0 1 .593-.592h6.815c.327 0 .593.265.593.592v3.408a4 4 0 0 1-4 4H5.926a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.445-4.444h8.296Z"/></svg></a>
        </div>
      </el-card>
      <el-card shadow="never" class="help">
        <div>Do not have an account? <RouterLink to="/register">Create one</RouterLink>.</div>
        <div>Forgot password? <RouterLink to="/forgot">Reset password</RouterLink>.</div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/sytle/user.css";
</style>