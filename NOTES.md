<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta/>
<meta/>
<meta/>
<title>Informed Delivery</title>
<meta/>
<meta/>
<style type="text/css">
      /* Dark Mode media queries to target Apple Mail, some Android and Outlook.com */
      @media (prefers-color-scheme: dark) {
        .img-dark-mode,
        .multi-envelope-icon-dark-mode,
        .x_img-dark-mode,
        .x_multi-envelope-icon-dark-mode {
          filter: invert(100%) sepia(100%) saturate(0) hue-rotate(204deg)
            brightness(103%) contrast(104%);
        }
        .primary-background-color {
          background: linear-gradient(#3573b1, #3573b1);
        }
        .secondary-background-color {
          background: linear-gradient(#336, #336);
        }
        .header-font-colors {
          color: #fffffe !important;
        }
        .dark-mode-section {
          background: linear-gradient(#2a2a32, #2a2a32);
          background-color: #2a2a32;
          color: #fffffe !important;
        }
        .primary-font-color,
        .responsive-header {
          color: #fffffe !important;
        }
        .secondary-font-color {
          color: #fffffe !important;
        }
        .tracking-number a {
          color: #fffffe !important;
        }
        .estimated-delivery {
          color: #fffffe !important;
        }
        .warning-message {
          color: #fffffe !important;
        }
        .linkable-text {
          color: #fffffe !important;
          -webkit-text-fill-color: #fffffe !important;
          text-decoration: none !important;
        }
      }
      /* DARK Mode END */
      .primary-background-color {
        background-color: #336;
      }
      .secondary-background-color {
        background-color: #3573b1;
      }
      .header-font-colors {
        color: #336;
      }
      .dark-mode-section {
        background-color: #f7f7f7;
        color: #000001;
      }
      .from-section-desktop {
        border-bottom: 2px solid #b8b8b8;
      }
      .from-section-mobile {
        background-color: #f7f7f7;
        border-bottom: none;
      }
      .primary-font-color,
      .responsive-header {
        color: #336;
      }
      .secondary-font-color {
        color: #000001;
      }
      .email-box-shadow {
        box-shadow: 0 8px 4px -4px#dee2e6 !important;
      }
      .mobile {
        display: none;
      }
      .expected-items-total {
        background-color: #336 !important;
        min-width: 80px;
        padding: 10px 8px 8px 8px;
        margin: 0;
        font-size: 15px;
        text-align: center;
        color: #fffffe !important;
        border-radius: 12px;
        font-weight: 400 !important;
      }
      .linkable-text {
        color: #000001;
        text-decoration: none !important;
      }
      .linkable-text:focus {
        outline: 3px solid #52addb !important;
      }
      .primary-button {
        background-color: #333367 !important;
        border: none !important;
        border-radius: 3px;
        color: #fffffe !important;
        display: inline-block;
        font-size: 16px;
        line-height: 44px;
        text-align: center;
        text-decoration: none;
        width: 225px;
        -webkit-text-size-adjust: none;
        white-space: nowrap;
        -webkit-text-size-adjust: none;
        height: 42px;
        font-weight: 700;
        font-family: Arial, Helvetica, sans-serif;
        vertical-align: middle !important;
        margin-right: 20px;
      }
      .view-dashboard-a,
      .x_view-dashboard-a {
        text-decoration: none !important;
      }
      a[class~="view-dashboard-a"] {
        text-decoration: none !important;
      }
      .view-dashboard-button {
        border-radius: 3px;
        padding: 9px 10px;
        border: 1px solid #fffffe !important;
        text-decoration: none !important;
        cursor: pointer;
        text-align: center;
        font-weight: 700;
        font-size: 16px;
        height: 44px;
        color: #fffffe !important;
        width: 200px;
        white-space: nowrap;
      }
      .view-dashboard-button:focus {
        outline: 4px solid #52addb;
      }
      .secondary-button {
        border: 1px solid #336;
        background-color: #fffffe !important;
        border-radius: 3px;
        color: #336 !important;
        display: inline-block;
        font-size: 16px;
        line-height: 44px;
        text-align: center;
        text-decoration: none;
        width: 225px;
        -webkit-text-size-adjust: none;
        white-space: nowrap;
        -webkit-text-size-adjust: none;
        height: 42px;
        font-weight: 700;
        font-family: Arial, Helvetica, sans-serif;
        vertical-align: middle !important;
        margin-right: 20px;
      }
      .expected-items-total {
        background-color: #336 !important;
        min-width: 80px;
        padding: 10px 8px 8px 8px;
        margin: 0;
        font-size: 15px;
        text-align: center;
        color: #fffffe !important;
        border-radius: 12px;
        font-weight: 400 !important;
      }
      .more-mail {
        border-bottom: 2px solid #999;
        padding-bottom: 5px;
      }
      .more-mail p {
        font-size: 12px;
      }
      .legal p {
        font-size: 11px;
      }
      .legal td {
        color: #000001 !important;
      }
      .legal td a {
        color: #3573b1 !important;
      }
      .tracking-number {
        font-size: 16px;
        font-weight: 700;
      }
      .estimated-delivery {
        font-size: 16px;
      }
      .warning-message {
        border-left: 10px solid #d4352d !important;
        padding-left: 15px;
        margin-right: 25px;
        line-height: 22px;
        margin-top: 0;
      }
      body,
      html {
        margin: 0 !important;
        padding: 0 !important;
        -webkit-text-size-adjust: none;
      }
      .custom-email-doc {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        font-weight: 400;
        display: block;
        margin: 0 auto;
        max-width: 800px;
      }
      hr {
        clear: both;
        display: block;
        height: 2px;
        background-color: #b8b8b8 !important;
        border-top-width: 0;
        border-right-width: 0;
        border-bottom-width: 0;
        border-left-width: 0;
        border-top-style: none;
        border-right-style: none;
        border-bottom-style: none;
        border-left-style: none;
        margin-top: 0;
        margin-right: 0;
        margin-bottom: 0;
        margin-left: 0;
      }
      h2 {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 21px;
        font-weight: 700;
        margin: 0;
        padding: 5px 0;
      }
      .header h1 {
        font-size: 33px;
        font-weight: 700;
      }
      .header tbody tr td a img {
        padding-left: 30px;
      }
      .refer {
        border-top: 2px solid #999 !important;
      }
      .refer button {
        margin-right: 20px;
        margin-bottom: 20px;
      }
      @media screen and (max-width: 768px) {
        h2.section-heading {
          font-size: 17px !important;
        }
        .desktop {
          mso-hide: all !important;
          display: none !important;
        }
        .mobile {
          display: block !important;
        }
        .mobile-button {
          border: none !important;
          text-decoration: underline !important;
          font-weight: 400 !important;
        }
        .responsive-header {
          font-size: 18px !important;
          margin-right: auto !important;
        }
        .responsive-header-logo {
          margin-left: auto !important;
        }
        .from-section-desktop {
          border-bottom: none !important;
          border-top-right-radius: 18px;
        }
        .from-section-mobile {
          border-bottom: 2px solid #b8b8b8 !important;
        }
        .img-container img {
          width: 100%;
        }
        .primary-button {
          width: 100% !important;
          margin-bottom: 20px;
          margin-right: 0 !important;
        }
        .secondary-button {
          width: 100% !important;
          margin-top: 0 !important;
          margin-right: 0 !important;
        }
        .refer button {
          margin-right: 0 !important;
        }
        .referButtons {
          text-align: center !important;
          margin-left: 0 !important;
        }
        #refer-email-link,
        #refer-text-link,
        .refer-email-button,
        .refer-text-button {
          text-align: center !important;
          margin-left: 0 !important;
          display: block !important;
          width: 100% !important;
        }
        .img-container img {
          width: 100%;
        }
        .view-dashboard-button,
        a.view-dashboard-button {
          border: none !important;
          text-decoration: underline !important;
          font-weight: 400 !important;
        }
        .section-header-title,
        .x_section-header-title {
          font-size: 23px !important ;
        }
        h1[class~="section-header-title"] {
          font-size: 23px !important;
        }
        td[class~="td-view-dash"] {
          padding-right: 8px !important;
        }
        .td-view-dash,
        .x_td-view-dash {
          padding-right: 8px !important;
        }
      }
      /* Override only the heading size for <=430px, 15px max to prevent wrapping */
      @media screen and (max-width: 430px) {
        h2.section-heading {
          font-size: 15px !important;
        }
      }
    </style>
</head>
<body>
<p>
<br/>
<img alt="" height="0" src="http://pixel.watch/1ewx" style="display: none; visibility: hidden" width="0"/> <img alt="" height="0" id="email-tracking-href-id" src="https://informeddelivery.usps.com/tracking/emailRead?emailToken=989e1620-6f77-4b4e-94a1-c73bbfcc45eb&amp;sentTime=2026-08-17T17:07:27.242Z&amp;deliveryDate=2026-08-17T05:00:00.000Z&amp;origin=cloudDigest" style="display: none; visibility: hidden" width="0"/> <img alt="" height="0" id="cloud-email-read-href-id" src="https://informeddelivery.usps.com/trackingV2/digest/open?a=rdcbx4zlbIphs0RwQxTKFmt1WZ9EFHHyvjH5lf67BeCxi69yZv7sBTjYgh56KO0Hes28oIzD2SdNkLk6Q_4jDEy6Q4R8o3zc3qCfOg4VDnxzzq5IfWoIV-DQfyBWiDrbAkhXG3czLS4LCUHA9Ab-oA0yZv0XeTbQ3RGkIDwcLE0yhq9T81SKwaSJHg" style="display: none; visibility: hidden" width="0"/>
</p>
<style>
      @media screen and (max-width: 768px) {
        h2.section-heading {
          font-size: 17px !important;
        }
        .desktop {
          mso-hide: all !important;
          display: none !important;
        }
        .mobile {
          display: block !important;
        }
        .mobile-button {
          border: none !important;
          text-decoration: underline !important;
          font-weight: 400 !important;
        }
        .responsive-header {
          font-size: 18px !important;
          margin-right: auto !important;
        }
        .responsive-header-logo {
          margin-left: auto !important;
        }
        .from-section-desktop {
          border-bottom: none !important;
          border-top-right-radius: 18px;
        }
        .from-section-mobile {
          border-bottom: 2px solid #b8b8b8 !important;
        }
        .img-container img {
          width: 100%;
        }
        .primary-button {
          width: 100% !important;
          margin-bottom: 20px;
          margin-right: 0 !important;
        }
        .secondary-button {
          width: 100% !important;
          margin-top: 0 !important;
          margin-right: 0 !important;
        }
        .refer button {
          margin-right: 0 !important;
        }
        .referButtons {
          text-align: center !important;
          margin-left: 0 !important;
        }
        #refer-email-link,
        #refer-text-link,
        .refer-email-button,
        .refer-text-button {
          text-align: center !important;
          margin-left: 0 !important;
          display: block !important;
          width: 100% !important;
        }
        .img-container img {
          width: 100%;
        }
        .view-dashboard-button,
        a.view-dashboard-button {
          border: none !important;
          text-decoration: underline !important;
          font-weight: 400 !important;
        }
        .section-header-title,
        .x_section-header-title {
          font-size: 23px !important ;
        }
        h1[class~="section-header-title"] {
          font-size: 23px !important;
        }
        td[class~="td-view-dash"] {
          padding-right: 8px !important;
        }
        .td-view-dash,
        .x_td-view-dash {
          padding-right: 8px !important;
        }
      }
      /* Override only the heading size for <=430px */
      @media screen and (max-width: 430px) {
        h2.section-heading {
          font-size: 15px !important;
        }
      }
    </style>
<div>
<table>
<tbody>
<tr>
<td>
<table>
<tbody>
<tr>
<td><img alt="USPS Logo" height="36" src="https://www.usps.com/email/id/uspslogo.png" width="64"/></td>
</tr>
<tr>
<td>
<h1>COMING TO YOU SOON</h1></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<h2>Hi<span>, MICHAEL</span>!</h2>
<p>You have <span>4</span> mailpiece(s) and <span>0</span> inbound package(s) arriving soon.</p>
<h2>Monday</h2>
<table>
<tbody>
<tr>
<td><span>17</span></td>
<td>
<div>August</div>
<div>2026</div>
</td>
</tr>
<tr>
<td> </td>
</tr>
</tbody>
</table>
</td>
<td>
<table>
<tbody>
<tr>
<td>
<h1>4</h1>
<p><strong>Mailpiece(s)</strong></p>
</td>
<td> </td>
<td>
<h1>0</h1>
<p><strong>Package(s)</strong></p>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<h2>Hi<span>, MICHAEL</span>!</h2>
<p>You have <span>4</span> mailpiece(s) and <span>0</span> inbound package(s) arriving soon.</p>
</td>
</tr>
<tr>
<td>
<table>
<tbody>
<tr>
<td>
<h1>Aug</h1>
<h1><strong></strong> 17</h1>
</td>
<td>
<h1>4</h1>
<p><strong>Mailpiece(s)</strong></p>
</td>
<td>
<h1>0</h1>
<p><strong>Package(s)</strong></p>
</td>
</tr>
<tr></tr>
</tbody>
</table>
</td>
</tr>
<tr></tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<div>
<table>
<tbody>
<tr>
<td><a href="#" id="mailbox-url-icon"> <img alt="Icon Envelope" height="34" src="https://www.usps.com/email/id/icon-envelope.png" style="
                            filter: saturate(1000%) brightness(1003%) !important;
                            width: 50px !important;
                            min-width: 50px;
                          " width="50"/> </a></td>
<td><span>
<h1>  MAIL</h1>
</span></td>
<td><a class="view-dashboard-a" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFmvw1GVIGGSHXXlX3g-SIpjHJQi0xCcdkatnprURoEbNd7zaTG9YdAosGZCYzhf7m8bZldQLbFEmoS2c4HYw7h2x2NzEdm2m7Q2B97Kt2XvNUfPwGdbnt7oNHZCfuLeOMbcE4gaL5Z8ykJ89FCqso04_R916OcAyEEpQoBsUbpY-tZ_u3fDt1GxCH7MJiyQ" id="mailbox-url-link" style="text-decoration: none"> <span>View Dashboard</span> </a></td>
</tr>
</tbody>
</table>
<div>
<table>
<tbody>
<tr>
<td>
<h2>Expected Today</h2>
</td>
<td>
<p> <span>4</span> <span>item(s)</span> </p>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<p>FROM: <b><span>Citibank</span></b></p>
</td>
</tr>
<tr>
<td>
<div>
<a href="" id="ra-representative-href-id" tabindex="0" target="_blank" title="Please visit this website for more info."> <img alt="campaign" id="campaign-representative-image-src-id" src="cid:1011420494-026.jpg"/></a>
</div>
</td>
</tr>
</tbody>
</table>
<div>
<table>
<tbody>
<tr>
<td>
<p><b><a class="primary-font-color" href="https://informeddelivery.usps.com/trackingV2/digest/mcClick?a=vY1JMW3J_Z0eehbqEERmaPtAsy1D2LWlNAp6pQEPwFsBcRy_-9T5cIO193gWNSnX0l6yZKggdl0dHECuiWYbjauJe8VsVM0ti4dyiYINmE8ivXtofKpSo1Ildqz0Kt4RslTQNU2yCjXhyJvmqu5mYiEzCxHSKpwlhjg5msIct1PIyNjejlwiBJ7BhX-MPzzyOkz3sOT3anxlE9cIjpn_FgR4yjgnmpsjKmgQbA6JKfafiLUUNBtSTvzLgBtDbfdTga4dqW19H2yIKjxntSTBxyMQcpTdvTpVMfc1_r1El_2tyY3v2_wlF0cQF5poaXN1XPxL0u596Tc1X3sx0co8Fq-gfh3rz-Zd8b-elv1fQkupFT5mkomA6qwGQKvmmG8tYPzQruQQBLg_-X1IoAZ2CLAifT6CIMGd54ukOmBJtqwZ6DJHd6gTD2ayiU8422O06lfVG0B2faUt_IsiiY7B0szzj3QfVl7VTdLOqzqy5sd_J7BZUcnqt5S9tljoLK8bKDdPcuFPzx-llVYfZV5puRT8-8xvvpAkaW1ja-jHLbWddgc9E_UaCF2ki-m9aFHJXUuVc84dhA7AAgrjlwEo9RCeNRHtKufR83d5Kwsr4QmrrTkm4Ts7P2MDiR-AyfkzB7SL8VC7hGcsV0tELAyudxqv2aSRvReBiF1GYs-vzOt3MC7aO91JGAkYN29bfLe-CwxuvQsg3wVvKaz675QAjsu16eoRDzke3uMAdv3Nx_xjAYgktDQenssYjf9f" id="ra-know-more-href-id" style="color: #333366;text-decoration:none !important;">Learn more about your mail <span> ❯</span> </a></b></p>
<a href="https://informeddelivery.usps.com/trackingV2/digest/mcClick?a=z1QKg3fIPtob6cexJbd0kZvVvRzuJ4OAgyryjM-hXXFPlaG8_oPkM-PSr9VEgjarQZm90eVCJcRQhw1rALSWTJzHK_zE4cvbcF23Hw82LDvdrXd82ZLnehqh-WXLnIC_YhSLje5AC6rsg8gQX6xeyVRox9HAPsRAUqRoCRsCMjVSvN-VyU1t5f5k4mylAtQ1xx4puiFdkyUO_rryB_5Wo9wUyHw75lUpYi8vK1QQS4Y9WAFz-mUWgky-q_EZEa3K_Xlel-EOcT6RF2AzM2zzvFC8Iun8t9V83i9tkp9KzRPA734S6--mUYct6TgZPJ__XUKaTe4t03W-6qSFel23oYDbNBdCkE3A72npekz8hEZ7cgnaPkNZNjBfZIGGV6s0821T-lCPNQgq4vwio8GTNs6O8ggLh_Mn9KfwmraMB_17qiUPv-G1ij6Boftmqw2RDfCI4ig9o-CWMpTmrdhgT40ik-rMzllPg55YDdh05JsWktwiOO5tdDsBc9hexcFRV_quYHKR0oNoSFWCivSjBiaVe88WN6xNGw4Aooizei72YR7oTkMtq-HW_IWmrpNdzgS6zoVy3TB0xWC3UFa5LHQk9D0EkekjBL_u5LDvYB1vG7ce4TjdYWUsk0U8Wf6Lzf-WDkEhhkRX3TrRJXU4Fs_dkdF_wR1B3nRGI3VcwO6pGZ82T6kvcvuKLYpvBo0C_r_5dcBKAdESAo5_cIqJzeONmZXLeSL4dxHc3Tvt-RiqaV5qtLMvyevV0tWMaxSHlyge" id="campaign-ridealong-image-href-id"><img alt="RideAlong image" id="campaign-ridealong-image-src-id" src="cid:content-1202017797.jpg" style="width: 300px;"/></a>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>
<table>
<tbody>
<tr></tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr></tr>
<tr>
<td>
<p><b><a class="primary-font-color" href="https://informeddelivery.usps.com/trackingV2/digest/mcClick?a=vY1JMW3J_Z0eehbqEERmaPtAsy1D2LWlNAp6pQEPwFsBcRy_-9T5cIO193gWNSnX0l6yZKggdl0dHECuiWYbjauJe8VsVM0ti4dyiYINmE8ivXtofKpSo1Ildqz0Kt4RslTQNU2yCjXhyJvmqu5mYiEzCxHSKpwlhjg5msIct1PIyNjejlwiBJ7BhX-MPzzyOkz3sOT3anxlE9cIjpn_FgR4yjgnmpsjKmgQbA6JKfafiLUUNBtSTvzLgBtDbfdTga4dqW19H2yIKjxntSTBxyMQcpTdvTpVMfc1_r1El_2tyY3v2_wlF0cQF5poaXN1XPxL0u596Tc1X3sx0co8Fq-gfh3rz-Zd8b-elv1fQkupFT5mkomA6qwGQKvmmG8tYPzQruQQBLg_-X1IoAZ2CLAifT6CIMGd54ukOmBJtqwZ6DJHd6gTD2ayiU8422O06lfVG0B2faUt_IsiiY7B0szzj3QfVl7VTdLOqzqy5sd_J7BZUcnqt5S9tljoLK8bKDdPcuFPzx-llVYfZV5puRT8-8xvvpAkaW1ja-jHLbWddgc9E_UaCF2ki-m9aFHJXUuVc84dhA7AAgrjlwEo9RCeNRHtKufR83d5Kwsr4QmrrTkm4Ts7P2MDiR-AyfkzB7SL8VC7hGcsV0tELAyudxqv2aSRvReBiF1GYs-vzOt3MC7aO91JGAkYN29bfLe-CwxuvQsg3wVvKaz675QAjsu16eoRDzke3uMAdv3Nx_xjAYgktDQenssYjf9f" id="ra-know-more-href-id-secondary" style="mso-hide:all;text-decoration:none !important;color: #333366;">Learn more about your mail <span> ❯</span> </a></b></p>
<a href="https://informeddelivery.usps.com/trackingV2/digest/mcClick?a=z1QKg3fIPtob6cexJbd0kZvVvRzuJ4OAgyryjM-hXXFPlaG8_oPkM-PSr9VEgjarQZm90eVCJcRQhw1rALSWTJzHK_zE4cvbcF23Hw82LDvdrXd82ZLnehqh-WXLnIC_YhSLje5AC6rsg8gQX6xeyVRox9HAPsRAUqRoCRsCMjVSvN-VyU1t5f5k4mylAtQ1xx4puiFdkyUO_rryB_5Wo9wUyHw75lUpYi8vK1QQS4Y9WAFz-mUWgky-q_EZEa3K_Xlel-EOcT6RF2AzM2zzvFC8Iun8t9V83i9tkp9KzRPA734S6--mUYct6TgZPJ__XUKaTe4t03W-6qSFel23oYDbNBdCkE3A72npekz8hEZ7cgnaPkNZNjBfZIGGV6s0821T-lCPNQgq4vwio8GTNs6O8ggLh_Mn9KfwmraMB_17qiUPv-G1ij6Boftmqw2RDfCI4ig9o-CWMpTmrdhgT40ik-rMzllPg55YDdh05JsWktwiOO5tdDsBc9hexcFRV_quYHKR0oNoSFWCivSjBiaVe88WN6xNGw4Aooizei72YR7oTkMtq-HW_IWmrpNdzgS6zoVy3TB0xWC3UFa5LHQk9D0EkekjBL_u5LDvYB1vG7ce4TjdYWUsk0U8Wf6Lzf-WDkEhhkRX3TrRJXU4Fs_dkdF_wR1B3nRGI3VcwO6pGZ82T6kvcvuKLYpvBo0C_r_5dcBKAdESAo5_cIqJzeONmZXLeSL4dxHc3Tvt-RiqaV5qtLMvyevV0tWMaxSHlyge" id="campaign-ridealong-image-href-id-secondary"> <img alt="RideAlong" id="campaign-ridealong-image-src-id-secondary" src="cid:content-1202017797.jpg" style="mso-hide:all;max-width: 300px"/> </a>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr></tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<table>
<tbody>
<tr></tr>
<tr></tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>
</div>
 </td>
</tr>
</tbody>
</table>
</div></td>
</tr>
</tbody>
</table>
</div>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<img alt="Mailpiece Image" id="mailpiece-image-src-id" src="cid:1011302269-026.jpg" style="padding-top:15px;"/>
</div>
</td>
</tr>
<tr>
<td> </td>
</tr>
</tbody>
</table>
</div>
   </td>
</tr>
</tbody>
</table>
</div></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<img alt="Mailpiece Image" id="mailpiece-image-src-id" src="cid:1011420406-026.jpg" style="padding-top:15px;"/>
</div>
</td>
</tr>
<tr>
<td> </td>
</tr>
</tbody>
</table>
</div>
   </td>
</tr>
</tbody>
</table>
</div></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
</div>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<table>
<tbody>
<tr>
<td>
<div>
<img alt="Mailpiece Image" id="mailpiece-image-src-id" src="cid:1011420384-026.jpg" style="padding-top:15px;"/>
</div>
</td>
</tr>
<tr>
<td> </td>
</tr>
</tbody>
</table>
</div>
   </td>
</tr>
</tbody>
</table>
</div></td>
</tr>
</tbody>
</table>
</div>
</td>
</tr>
</tbody>
</table>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td></td>
<td><img alt="multi envelope icon-dark-mode image" class="multi-envelope-icon-dark-mode" height="48" src="https://www.usps.com/email/id/multiple-envelopes-icon.png" style="
                              width: 53px !important;
                              height: 48px !important;
                              min-width: 53px !important;
                            " width="53"/></td>
<td>
<p>There is one or more mailpieces for which we do not currently have an image that is included in today's mail.</p></td>
</tr>
</tbody>
</table>
</div>
</div>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
</div>
</div>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td><a href="https://informeddelivery.usps.com/box/pages/secure/DashboardAction_input?keyword=pack" id="view-all-package-link-icon"> <img alt="Package Icon" height="36" src="https://www.usps.com/email/id/packages-icon.png" style="
                            filter: saturate(1000%) brightness(1003%) !important;
                            width: 46px !important;
                            max-width: 46px;
                          " width="46"/> </a></td>
<td><span>
<h1>  PACKAGES</h1>
</span></td>
<td><a class="view-dashboard-a" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFu4q3QODgQkk8ODfSfcIFDr0yF2yz_i8o2Vh5DzcIIMhNhoWUUeO4b8j14biN5lLzUS7D3Ud0fRY4tLUVrQNu3Q5-0T2Nn8PP4MriJbIV7haL4-NSyGFaieKF4VRUO1nt63DjzAE50R0Ws8GamIgsGmaRdr4eO4DkfkLL0s1pSugd6t3F1v_Tjo_qW46pwu9cqY" id="view-all-package-link-id" style="text-decoration: none"> <span>View Dashboard</span> </a></td>
</tr>
</tbody>
</table>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td><strong>No packages are available to display.</strong></td>
</tr>
</tbody>
</table>
</div>
<div></div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<div></div>
<div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<div></div>
</div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<div></div>
<table>
<tbody>
<tr>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td></td>
</tr>
<tr>
<td><img alt="footer banner" id="footer-banner-img-id" src="https://www.usps.com/email/id/refer-friends-and-family-banner.png" style="width: 100%"/></td>
</tr>
<tr>
<td></td>
</tr>
<tr>
<td>
<div>
<span>  <span> <a href="https://informeddelivery.usps.com/trackingV2/digest/referral?a=rdcbx4zlbIphs0RwQxTKFvmXpGu9S25pmHMWke1dFkEKsIqhLvnHwkuqYjAWrZ6hRdBl52wbH1stwPVeBkmG2JXVpZ6P-G1DZ2wSCXqv9ITe1SJgohr7_qs1Zw2mY7iArNqJbxBOCiLoz4oJQ-4dJmkFa-NDEGI5Qou0-ymFRObeRXMihgpdcR4UyjjWcINQG8G06g" id="refer-email-link" style="
                                background-color: #333367 !important;
                                border: none !important;
                                border-radius: 5px;
                                color: #fffffe !important;
                                display: inline-block;
                                font-family: sans-serif;
                                font-size: 16px !important;
                                line-height: 40px;
                                text-align: center;
                                text-decoration: none;
                                width: 225px;
                                -webkit-text-size-adjust: none;
                                white-space: nowrap;
                                -webkit-text-size-adjust: none;
                                min-height: 42px;
                                height: 42px;
                                max-height: 42px;
                                font-weight: bold !important;
                                font-family: Arial, Helvetica, sans-serif;
                                text-align: center;
                                vertical-align: middle !important;
                              " target="_blank">Refer via Email</a> </span>  </span>
<span>  <span> <a href="https://informeddelivery.usps.com/trackingV2/digest/referral?a=rdcbx4zlbIphs0RwQxTKFk4QCnVHvuZ__UjouKzQTzw8S7p__4E7sSlNejwNyo4_PQ3HIm3iagB0OY_sHmE8ie1u3gnk-ebzODFbk6UEoZzkwjqLGNMW8jEWin35aMIqsDY_efg744oXhG0gVg3Nu0hLuVetAd_2Zhkz3YZj4zQY63jfxpQOkGVzoSzM6XXoXWc" id="refer-text-link" style="
                                background-color: #fffffe !important;
                                border: none !important;
                                border-radius: 5px;
                                color: #333367 !important;
                                display: inline-block;
                                font-family: sans-serif;
                                font-size: 16px !important;
                                line-height: 40px;
                                text-align: center;
                                text-decoration: none;
                                width: 225px;
                                -webkit-text-size-adjust: none;
                                white-space: nowrap;
                                -webkit-text-size-adjust: none;
                                min-height: 42px;
                                height: 42px;
                                max-height: 42px;
                                font-weight: bold !important;
                                font-family: Arial, Helvetica, sans-serif;
                                text-align: center;
                                vertical-align: top !important;
                                overflow: hidden !important;
                                margin-left: 1px !important;
                                margin-right: 1px !important;
                              " target="_blank">Refer via Text</a> </span>  </span>
</div>
</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<p>You may have more mail or packages than are shown in your Daily Digest. To check, <strong><a class="anchored-text" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFtmeAO6xbhY-regAOKE5oodeXB0_2BMzjzvSMbge1GckM3OAIRAxTsbVe4kOZbGlwEsWyRdtS7wn2Z3eiuG2yBZwXfp8LHhG8tN6pnKpFJHpYkNo_bM1Ot3rveWTxqeVLODYMGsgnJAIQbm_NY6N8RKqvmP_lYms4tXt_MuJ4CJM06fa3A4ZDrWdDTxnOzL8yII" id="mailbox-url-link-2" style="
                              text-decoration: underline !important;
                              color: #3573b1;
                              font-weight: bold;
                            ">go to your Dashboard</a></strong>.</p>
<p>Mail may arrive after you receive the notification. Please allow several days for delivery before reporting missing mail. <strong><a class="anchored-text" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFmNymymrmOKu9zi_50B-keBke0m1GbCtkuOBhGYAE6QTEkWzqSW81eev_WsrmgZFgQEFQO6O0e8_hEET9yoNYzI3VzAaqpBNMiWdCc7A80ejJPrSYU7S9JDhP-7Vq5ZaY6DNwhez_rY0wWC2Lnh1ucblN2mlw9VuaSBFtvQPAaZrXufny0FHbYrFqWxl-psFUwKK" id="missing-mailpiece-href-id" style="
                              text-decoration: underline !important;
                              color: #3573b1;
                              font-weight: bold;
                            ">Sign in</a></strong> to your consumer dashboard to report missing mail within 7 days of receiving this Daily Digest email.</p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td>
<p>*These images represent mail pieces that are sorted on USPS<sup>®</sup> automated equipment. Some of your mail may not be shown here.</p>
<p>You subscribed to this service with USPS<sup>®</sup> Product Technology Innovation, 475 L`Enfant Plaza SW, Washington, DC 20260.</p>
<p>If you no longer wish to receive daily email notifications, <a class="anchored-text" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFiX_h_gi_Rmtwgc2OsJZTjAfsMoDWvzKH95HpHweAzdtreTJNXzayApF94Oe6aOfoKMw1wyFS7UGrJAezWgGc5Yu3ocO2fzPB3ypIOtmHXTBB8-w55RE4CLk2BJQGsfbyx_CJUEzzZmCIM14v3ku1hxH-8pQpdXY_NihWz7kztT-BwwqfEBGIb_f4Mbw-VXJT9l1a0txL6M1smf1DBgd69kHaZWyf-OybGy98zWVkKKbViycvnFzOn0" id="unsubscribe-url-link" style="
                            text-decoration: underline !important;
                            color: #3573b1;
                            font-weight: bold;
                          " target="_blank">unsubscribe here</a>.</p>
<p>If you need support, please visit <a class="anchored-text" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFlLGFUHRrBmOgH-G78hnJGMNIhs57r3KVQL1x_mVoicBvcC2AVPJsferZISPSNOBPmG1YcxRx0dOoVxQBvcvD7l0ZFAYpl9HkaU6dMzFlv1gamlzpK9XNMRTZtrzOGbMY8FfRMwgdwJzHwLcFevQLm7-aQEWfTtLFW8bxxp3BFWEzEM0D4jX78EB-YktKmIQKw" id="user-support-href-id" style="
                            text-decoration: underline !important;
                            color: #3573b1;
                            font-weight: bold;
                          " target="_blank">user support for Informed Delivery<sup>®</sup></a>.</p>
<p>For more information about this service, please visit <a class="anchored-text" href="https://informeddelivery.usps.com/trackingV2/digest/click?a=rdcbx4zlbIphs0RwQxTKFunywW_mIxQ3MuCtq0Yq06iuM0oLehVR_sn4r9e_fQzvHQV-StQ52PjJf7xVaJPn34oISWAHv7qaQcofE9zFef_G7TopnsNRIdQClN3Z5hRbWsOjH1Sm91vnPPsCzWsmDjDiYOZMMQ3_U8x6FRHNlhmwepmUaAXpRfcPLfm89uU975XSog" id="faq-href-id" style="
                            text-decoration: underline !important;
                            color: #3573b1;
                            font-weight: bold;
                          " target="_blank">general information about Informed Delivery</a>.</p>
<p>Copyright © <span>2026</span> United States Postal Service<sup>®</sup>. All Rights Reserved. The Eagle Logo and the trade dress of USPS<sup>®</sup> Packaging are among the many trademarks of the U.S. Postal Service<sup>®</sup>.</p>
<p>This is an automated email, please do not reply to this message. This message is for the designated recipient only and may contain privileged, proprietary, or otherwise private information. If you have received it in error, please delete. Any other use of the email by you is prohibited.</p></td>
</tr>
</tbody>
</table>
</div></td>
</tr>
</tbody>
</table>
</div>
</body>
</html>
